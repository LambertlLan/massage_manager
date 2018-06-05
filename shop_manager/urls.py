# __author: Lambert
# __date: 2018/5/18 14:55
from django.urls import path
from shop_manager import views

urlpatterns = [
    path('shopList/', views.ShopList.as_view()),
    path('symptomList/', views.SymptomList.as_view()),
    path('symptomInfo/', views.SymptomInfo.as_view()),
    path('cityList/', views.CityList.as_view()),
    path('technicianList/', views.TechnicianList.as_view()),

]
