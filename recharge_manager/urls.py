# __author: Lambert
# __date: 2018/5/25 9:42
from django.urls import path
from . import views

urlpatterns = [
    path("rechargeActive/", views.RechargeActive.as_view()),
    path("wx_pay/", views.Recharge.as_view()),
]
