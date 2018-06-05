# __author: Lambert
# __date: 2018/5/18 14:55
from django.urls import path
from . import views

urlpatterns = [
    path('issueVoucherCategoryId/', views.GetIssueVoucher.as_view()),
    path('receiveVoucher/', views.ReceiveVoucher.as_view()),

]
