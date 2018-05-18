import requests
import json
import random

from django.shortcuts import render
from django import views
from django.http import JsonResponse
from user_manager import models


class Base(views.View):
    """基类"""

    def __init__(self):
        super(Base, self).__init__()
        self.openid_url = "https://api.weixin.qq.com/sns/jscode2session"
        self.grant_type = "authorization_code"
        self.appid = "wx2c6cce1d511b3725"
        self.secret = "98387dd4a725445139ed91f7d411f1ee"
        self.res_json = {"code": 0, "msg": "success"}


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
        user_model = models.Customer.objects.filter(wx_id=openid)
        if user_model.count() > 0:
            if user_model[0].mobile:
                return True
            else:
                return False
        else:
            models.Customer.objects.create(wx_id=openid)
            return False


class GetMsgCode(Base):
    def get(self, request):
        msg_code = self.create_msg_code()
        self.res_json["msgCode"] = msg_code
        return JsonResponse(self.res_json)

    @staticmethod
    def create_msg_code():
        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        x = random.choice(chars), random.choice(chars), random.choice(chars), random.choice(chars)
        verify_code = "".join(x)
        return verify_code
