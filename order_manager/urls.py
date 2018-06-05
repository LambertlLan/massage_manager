# __author: Lambert
# __date: 2018/5/25 9:42
from django.urls import path
from order_manager import views

urlpatterns = [
    path("createOrder/", views.CreateOrder.as_view()),
    path("getOrderList/", views.GetOrderList.as_view())
]
