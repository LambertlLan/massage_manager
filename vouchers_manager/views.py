from django.shortcuts import render
from django.http import JsonResponse
from user_manager.views import Base
from . import models as vouchers_models
from user_manager import models as user_models


class GetIssueVoucher(Base):
    def get(self, request):
        issue_voucher_obj = vouchers_models.VouchersManager.objects.filter(is_issue=True)
        if issue_voucher_obj.count() > 0:
            issue_vouchers_id = issue_voucher_obj.order_by('-id')[0].id
            self.res_json["issue_vouchers_id"] = issue_vouchers_id
        else:
            self.res_json["code"] = 1
            self.res_json["msg"] = "当前暂无发放代金券"
        return JsonResponse(self.res_json)


class ReceiveVoucher(Base):
    def get(self, request):
        mobile = request.GET.get("mobile")
        issue_id = request.GET.get("issue_id")
        wx_id = request.GET.get("openid")
        is_issue = vouchers_models.VouchersManager.objects.get(id=issue_id).is_issue
        # 查询是否开放领取
        if not is_issue:
            self.res_json["code"] = 1
            self.res_json["msg"] = "领取时间已过"
        else:
            # 查询用户是否注册
            is_register = user_models.Customer.objects.filter(mobile=mobile).exists()
            if is_register:
                user_id = user_models.Customer.objects.get(mobile=mobile).id
                # 查询该分类该用户领取的数量
                user_receive_count = vouchers_models.Vouchers.objects.filter(user_id=user_id,
                                                                             voucher_id=issue_id).count()
                # 此处控制领取张数
                if user_receive_count >= 1:
                    self.res_json["code"] = 1
                    self.res_json["msg"] = "已领取该代金券"
                else:
                    vouchers_models.Vouchers.objects.create(user_id=user_id, voucher_id=issue_id)
            else:
                # 如果是新用户直接发放
                new_user_obj = user_models.Customer(mobile=mobile)
                new_user_obj.save()
                user_id = new_user_obj.id
                vouchers_models.Vouchers.objects.create(user_id=user_id, voucher_id=issue_id)
        return JsonResponse(self.res_json)
