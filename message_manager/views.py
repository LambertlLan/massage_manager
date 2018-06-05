from django.shortcuts import render
from django.http import JsonResponse
from user_manager.views import Base
from . import models as message_models


# Create your views here.
class GetMessageList(Base):
    def get(self, request):
        wx_id = request.GET.get("openid")
        message_list = message_models.MessageCenter.objects.filter(user__wx_id=wx_id).values()
        message_list = list(message_list)
        self.res_json["results"] = message_list
        return JsonResponse(self.res_json)
