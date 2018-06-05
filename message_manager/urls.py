# __author: Lambert
# __date: 2018/5/25 9:42
from django.urls import path
from message_manager import views

urlpatterns = [
    path("getMessageList/", views.GetMessageList.as_view())
]
