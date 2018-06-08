from django.shortcuts import render
from django.db.models import F
from django.http import JsonResponse, HttpResponse
from user_manager.views import Base
from recharge_manager import models as recharge_models
from massage_manager.settings import BASE_DIR
from user_manager import models as user_models
from wx_pay.wx_pay import WxPay
from order_manager import models as order_models

from xml.etree import ElementTree
import time
import os
import logging

logger = logging.getLogger(__name__)


class RechargeActive(Base):
    """充值活动"""

    def get(self, request):
        active_list = recharge_models.RechargeActive.objects.values()
        self.res_json["results"] = {"active_list": list(active_list)}
        return JsonResponse(self.res_json)


class Recharge(Base):
    """充值"""

    def post(self, request):
        wx_id = request.POST.get("openid")
        user_id = user_models.Customer.objects.get(wx_id=wx_id).id
        recharge_active_id = int(request.POST.get("rechargeActiveId"))
        recharge_active_obj = recharge_models.RechargeActive.objects.get(id=recharge_active_id)
        recharge_amount = recharge_active_obj.recharge_amount
        # 写入充值记录
        record_number = "CZ_%d" % int(round(time.time() * 1000))
        record_model = recharge_models.RechargeOrder(user_id=user_id, amount=recharge_amount,
                                                     record_number=record_number)
        record_model.save()
        # 调用微信统一下单接口
        wx_pay = WxPay()
        res_json = wx_pay.wx_create_order(wx_id, record_number, self.get_client_ip(request), recharge_amount,
                                          self.res_json)

        return JsonResponse(res_json)


# 微信支付回调
def payback(request):
    _xml = request.body
    # 拿到微信发送的xml请求
    xml = str(_xml, encoding="utf-8")
    return_dict = {}
    tree = ElementTree.fromstring(xml)
    # xml 解析
    return_code = tree.find("return_code").text
    try:
        if return_code == 'FAIL':
            # 官方发出错误
            return_dict['message'] = '支付失败'
        elif return_code == 'SUCCESS':
            # 拿到自己这次支付的 out_trade_no
            _out_trade_no = tree.find("out_trade_no").text
            order_number = _out_trade_no.split('-')[1]
            order_type = order_number.split('_')[0]
            total_fee = int(tree.find("total_fee").text) / 100
            if order_type == "CZ":
                """充值订单"""
                pay_type = recharge_models.RechargeOrder.objects.get(record_number=order_number).is_pay
                if not pay_type:
                    present_amount = recharge_models.RechargeActive.objects.get(
                        recharge_amount=total_fee).present_amount
                    # 改写充值订单状态
                    recharge_models.RechargeOrder.objects.filter(record_number=order_number).update(is_pay=True)
                    # 增加用户余额
                    user_id = recharge_models.RechargeOrder.objects.get(record_number=order_number).user_id
                    user_models.Customer.objects.filter(id=user_id).update(
                        balance=F("balance") + total_fee + present_amount)
                else:
                    logger.info(f"订单{order_number}支付状态已经变更,无须再此变更")
            elif order_type == "DD":
                """支付订单"""
                order_obj = order_models.Order.objects.get(order_number=order_number)
                pay_type = order_obj.is_pay
                if not pay_type:
                    # 检测支付金额和订单金额是否一致
                    if total_fee == order_obj.need_pay:
                        order_obj.is_pay = True
                        order_obj.save()
                    else:
                        logger.info(f"订单{order_number}支付金额不一致")
                else:
                    logger.info(f"订单{order_number}支付状态已经变更,无须再此变更")

    except Exception as e:
        logger.info(e)
    finally:

        return HttpResponse(open(os.path.join(BASE_DIR, 'wx_pay/pay_success.xml'), "r"), content_type="text/xml")
