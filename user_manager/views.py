import requests
import json
import random
import time
import datetime
import logging

from django.shortcuts import render
from django import views
from django.http import JsonResponse
from user_manager import models as user_models
from vouchers_manager import models as vouchers_models
from recharge_manager import models as recharge_models
from order_manager import models as shop_models
from message_manager import models as message_models
from utils.send_msg import send_sms

logger = logging.getLogger(__name__)


class Base(views.View):
    """基类"""

    def __init__(self):
        super(Base, self).__init__()
        self.openid_url = "https://api.weixin.qq.com/sns/jscode2session"
        self.grant_type = "authorization_code"
        self.appid = "wxf017ba90c650cadd"
        self.secret = "b02cba99aed59341e270ee1e05f6513a"
        self.res_json = {"code": 0, "msg": "success"}

    @staticmethod
    def get_client_ip(request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
            regip = real_ip.split(",")[0]
        except:
            try:
                regip = request.META['REMOTE_ADDR']
            except:
                regip = ""
        return regip


class Login(Base):
    """登录"""

    def post(self, request):
        code = request.POST.get("code")
        res_data = self.get_open_id(code)
        self.res_json["openid"] = res_data["openid"]
        if not self.check_first_login(res_data["openid"]):
            self.res_json["first_login"] = 1
        return JsonResponse(self.res_json)

    def get_open_id(self, code):
        res_msg = requests.get(self.openid_url,
                               {"appid": self.appid, "secret": self.secret,
                                "grant_type": self.grant_type, "js_code": code})
        res_data = json.loads(res_msg.text)
        return res_data

    @staticmethod
    def check_first_login(openid):
        user_model = user_models.Customer.objects.filter(wx_id=openid)
        if user_model.count() > 0:
            if user_model[0].mobile:
                return True
            else:
                return False
        else:
            user_models.Customer.objects.create(wx_id=openid)
            return False


class Register(Base):
    """注册"""

    def post(self, request):
        mobile = request.POST.get("mobile")
        msg_code = request.POST.get("msgCode")
        openid = request.POST.get("openid")
        if GetMsgCode.check_msg_code(mobile, msg_code):
            # 检测该用户是否未注册但领取过代金券
            has_voucher = user_models.Customer.objects.filter(mobile=mobile).exists()
            if has_voucher:
                # 如果存在,删除当前用openid注册的用户数据,将openid写到存在的数据中
                user_models.Customer.objects.filter(wx_id=openid).delete()
                user_models.Customer.objects.filter(mobile=mobile).update(wx_id=openid)
            else:
                user_models.Customer.objects.filter(wx_id=openid).update(mobile=mobile)
            # 写入消息列表
            user_id = user_models.Customer.objects.get(wx_id=openid).id
            message_models.MessageCenter.objects.create(user_id=user_id, content="欢迎新用户注册")
        else:
            self.res_json["code"] = 1
            self.res_json["msg"] = "验证码不正确"
        return JsonResponse(self.res_json)


class GetMsgCode(Base):
    """获取验证码"""

    def get(self, request):
        mobile = request.GET.get("mobile")
        msg_code = self.create_msg_code()
        if user_models.MsgCode.objects.filter(mobile=mobile).exists():
            obj = user_models.MsgCode.objects.get(mobile=mobile)
            obj.msg_code = msg_code
            obj.save()
        else:
            user_models.MsgCode.objects.create(mobile=mobile, msg_code=msg_code)
        logger.info(f"{mobile}获取验证码{msg_code}")
        send_msg_res = send_sms(mobile, msg_code)
        send_msg_res = json.loads(send_msg_res)
        if send_msg_res["code"] != 2:
            self.res_json["code"] = 1
            self.res_json["msg"] = "短信接口返回出错"
        return JsonResponse(self.res_json)

    @staticmethod
    def create_msg_code():
        """生成验证码"""
        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        x = random.choice(chars), random.choice(chars), random.choice(chars), random.choice(chars)
        verify_code = "".join(x)
        return verify_code

    @staticmethod
    def check_msg_code(mobile, msg_code):
        """验证验证码"""
        msg_obj = user_models.MsgCode.objects.filter(mobile=mobile, msg_code=msg_code)
        if msg_obj.count() > 0:
            create_time = msg_obj[0].create_time
            un_time = time.mktime(create_time.timetuple())
            # 验证码有效期五分钟
            if int(time.time()) - un_time > 60 * 5:
                return False
            else:
                return True
        else:
            return False


class Account(Base):
    """我的账户"""

    def get(self, request):
        wx_id = request.GET.get("openid")

        user_id = user_models.Customer.objects.get(wx_id=wx_id).id
        balance = user_models.Customer.objects.get(wx_id=wx_id).balance

        recharge_record = recharge_models.RechargeOrder.objects.filter(user_id=user_id, is_pay=True).values()
        current_time = datetime.datetime.now()
        vouchers = vouchers_models.Vouchers.objects.filter(user_id=user_id, is_used=False,
                                                           voucher__effective_time__gte=current_time).values("id",
                                                                                                             "voucher",
                                                                                                             "voucher__effective_time",
                                                                                                             "voucher__amount")
        for voucher in vouchers:
            voucher_category_id = voucher["voucher"]
            shops = vouchers_models.VouchersManager.objects.get(id=voucher_category_id).belong_shop.values("shop_name")
            voucher["belong_shops"] = list(shops)

        expend_record = shop_models.Order.objects.filter(user_id=user_id, is_pay=True, pay_type='0').values("id",
                                                                                                            "date",
                                                                                                            "need_pay",
                                                                                                            "shop__shop_name",
                                                                                                            "order_number")
        results = {
            "expend_record": list(expend_record),
            "vouchers": list(vouchers),
            "recharge_record": list(recharge_record)
        }
        self.res_json["balance"] = balance
        self.res_json["results"] = results
        return JsonResponse(self.res_json)
