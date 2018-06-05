"""massage_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 处理favicon.ico
from django.views.generic.base import RedirectView
import xadmin

urlpatterns = [
                  # index
                  path('', RedirectView.as_view(url='/mini-manager/')),
                  # xadmin
                  path('mini-manager/', xadmin.site.urls),
                  # favicon.ico
                  path('favicon.ico/', RedirectView.as_view(url=r'static/favicon.ico')),

                  # user
                  path('user/', include("user_manager.urls")),
                  # shop
                  path('shop/', include("shop_manager.urls")),
                  # message
                  path('message/', include("message_manager.urls")),
                  # order
                  path('order/', include("order_manager.urls")),
                  # recharge
                  path('recharge/', include("recharge_manager.urls")),
                  # voucher
                  path('voucher/', include("vouchers_manager.urls"))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 配置媒体文件路径
