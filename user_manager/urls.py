# __author: Lambert
# __date: 2018/5/18 14:55
from django.urls import path
from user_manager import views

urlpatterns = [
    path('login/', views.Login.as_view()),
    path('register/', views.Register.as_view()),
    path('getMsgCode/', views.GetMsgCode.as_view()),
    path('account/', views.Account.as_view()),

]
