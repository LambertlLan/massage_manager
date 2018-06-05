from django.shortcuts import render
from django.db.models import F
from django.http import JsonResponse
from user_manager.views import Base
from recharge_manager import models as recharge_models
from user_manager import models as user_models
import time


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
        present_amount = recharge_active_obj.present_amount
        # 写入充值记录
        record_model = recharge_models.RechargeOrder(user_id=user_id, amount=recharge_amount,
                                                     record_number="CZ_%d" % int(round(time.time() * 1000)))
        record_model.save()
        record_id = record_model.id
        # 调用微信支付

        # 改写充值记录状态
        recharge_models.RechargeOrder.objects.filter(id=record_id).update(is_pay=True)
        # 写入客户数据
        user_models.Customer.objects.filter(wx_id=wx_id).update(balance=F("balance") + recharge_amount + present_amount)

        return JsonResponse(self.res_json)
