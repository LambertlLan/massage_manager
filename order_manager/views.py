from django.shortcuts import render
from django.http import JsonResponse
from user_manager.views import Base
from user_manager import models as user_models
from vouchers_manager import models as voucher_models
from shop_manager import models as shop_models
from . import models as order_models
from wx_pay.wx_pay import WxPay
import json
import time


class CreateOrder(Base):
    """下单接口"""

    def __init__(self):
        super(CreateOrder, self).__init__()
        self.wx_id = None
        self.shop_id = None
        self.pay_type = None
        self.total_price = None
        self.need_pay = None
        self.use_vouchers = None
        self.voucher_id = None
        self.voucher_amount = None
        self.order_id = None
        self.program_list = []
        self.pro_tech_models = []
        self.order_number = None

    def post(self, request):
        req_dict = request.POST.dict()
        self.pay_type = req_dict["pay_type"]
        self.wx_id = req_dict["openid"]
        self.program_list = json.loads(req_dict["cart_list"])
        self.shop_id = self.program_list[0]["shopId"]
        # 项目总价
        self.total_price = self.calculate_total_price()
        self.need_pay = self.total_price
        # 是否使用代金券
        self.use_vouchers = req_dict["use_vouchers"]
        if self.use_vouchers == '1':
            self.voucher_id = req_dict["voucher_id"]
            voucher_obj = voucher_models.Vouchers.objects.get(id=self.voucher_id)
            self.voucher_amount = voucher_obj.voucher.amount
            self.need_pay = self.total_price - self.voucher_amount
            if self.need_pay < 0:
                self.need_pay = 0
            voucher_obj.is_used = True
            voucher_obj.save()
        # 余额支付
        if self.pay_type == '0':
            self.balance_pay()
        # 微信支付
        elif self.pay_type == "1":
            self.res_json = self.wx_pay(self.get_client_ip(request))

        return JsonResponse(self.res_json)

    # 计算总价,并将模型添加到self.pro_tech_models中
    def calculate_total_price(self):
        total_price = 0
        for item in self.program_list:
            program_id = item["programId"]
            technicial_id = item["technicial"]["id"]
            pro_model = shop_models.MassageProgram.objects.get(id=program_id)
            need_time = pro_model.need_time
            technicial_model = shop_models.Technician.objects.get(id=technicial_id)
            self.pro_tech_models.append(
                {"tech_model": technicial_model, "pro_model": pro_model, "start_time": item["arriveTime"],
                 "end_time": item["endTime"]})
            technicial_price = technicial_model.price
            total_price = total_price + (need_time * technicial_price)
        return total_price

    # 微信支付
    def wx_pay(self, ip):
        # 创建订单
        self.create_order()
        # 发起微信支付
        # 调用微信统一下单接口
        wx_pay = WxPay()
        res_json = wx_pay.wx_create_order(self.wx_id, self.order_number, ip, self.need_pay, self.res_json)
        # 写入预约列表
        self.create_reservation_record()

        return res_json

    # 余额支付
    def balance_pay(self):
        user_balance = user_models.Customer.objects.get(wx_id=self.wx_id).balance
        if user_balance < self.need_pay:
            self.res_json["code"] = 1
            self.res_json["msg"] = "余额不足"
        else:
            # 创建订单
            self.create_order()
            # 扣除余额
            user_models.Customer.objects.filter(wx_id=self.wx_id).update(balance=user_balance - self.need_pay)
            # 改写订单支付状态
            self.change_order_pay_status(self.order_id)
            # 写入预约列表
            self.create_reservation_record()

    # 开始创建订单
    def create_order(self):
        self.order_number = "DD_%d" % int(round(time.time() * 1000))
        user_model = user_models.Customer.objects.get(wx_id=self.wx_id)
        shop_model = shop_models.Shop.objects.get(id=self.shop_id)
        amount = self.total_price
        voucher_model = None
        if self.voucher_id:
            voucher_model = voucher_models.Vouchers.objects.get(id=self.voucher_id)
        obj = order_models.Order(order_number=self.order_number, user=user_model, shop=shop_model, amount=amount,
                                 need_pay=self.need_pay, voucher=voucher_model, pay_type=self.pay_type)
        obj.save()
        self.order_id = obj.id

        for model in self.pro_tech_models:
            # 将项目模型添加到订单中
            obj.program.add(model["pro_model"])
            # 将技师模型添加到订单中
            obj.technician.add(model["tech_model"])

        obj.save()

    # 改写订单支付状态
    @staticmethod
    def change_order_pay_status(order_id):
        order_models.Order.objects.filter(id=order_id).update(is_pay=True)

    # 创建预约记录
    def create_reservation_record(self):
        order_model = order_models.Order.objects.get(id=self.order_id)
        for model in self.pro_tech_models:
            order_models.ReservationRecord.objects.create(order=order_model, program=model["pro_model"],
                                                          technician=model["tech_model"],
                                                          start_time=model["start_time"], end_time=model["end_time"])


class GetOrderList(Base):
    def get(self, request):
        wx_id = request.GET.get("openid")
        orders = order_models.Order.objects.filter(user__wx_id=wx_id, is_pay=True).values("id", "amount",
                                                                                          "shop__shop_name",
                                                                                          "complete",
                                                                                          "date")

        for item in orders:
            # 查询技师和项目
            obj = order_models.Order.objects.get(id=item["id"])
            item["programs"] = list(obj.program.values("program_name"))
            item["technicians"] = list(obj.technician.values("real_name"))
            # 查询预约时间
            item["start_time"] = order_models.ReservationRecord.objects.filter(order_id=item["id"])[0].start_time
            item["end_time"] = order_models.ReservationRecord.objects.filter(order_id=item["id"])[0].end_time

        self.res_json["results"] = {"orders": list(orders)}
        return JsonResponse(self.res_json)
