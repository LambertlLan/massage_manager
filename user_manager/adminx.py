# __author: Lambert
# __date: 2018/5/18 10:55
# Register your models here.


import xadmin

from xadmin.sites import site
from xadmin import views
from .models import Customer
from django.shortcuts import render

# menus
from order_manager.adminx import order_menu
from shop_manager.adminx import shop_menu
from message_manager.adminx import message_menu
from vouchers_manager.adminx import vouchers_menu
from recharge_manager.adminx import recharge_menu
from xadmin.views import BaseAdminView
from xadmin.views import CommAdminView


class GlobalSetting(object):
    """xadmin全局配置"""
    # 设置base_site.html的Title
    site_title = 'MASSAGE MANAGER'
    # 设置base_site.html的Footer
    site_footer = 'MASSAGE后台管理系统'
    # 设置折叠菜单
    menu_style = "accordion"

    def get_site_menu(self):
        menus = []
        menus.extend(shop_menu(self))
        menus.extend(user_menu(self))
        menus.extend(order_menu(self))
        menus.extend(recharge_menu(self))
        menus.extend(message_menu(self))
        menus.extend(vouchers_menu(self))

        return menus


class BaseSetting(object):
    enable_themes = True  # 打开主题功能
    use_bootswatch = True  #


class MapView(CommAdminView):

    def get(self, request):
        content = self.get_context()
        return self.template_response("map.html", content)


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
site.register_view('map/', MapView, name='map')


def user_menu(obj):
    menus = [
        {
            'title': '用户管理',
            'perm': obj.get_model_perm(Customer, 'change'),
            'icon': 'fa fa-user',
            'menus': (
                {'title': '用户列表', 'icon': 'fa fa-user-secret ',
                 'url': obj.get_model_url(Customer, 'changelist')},
            )
        }
    ]
    return menus


class CustomerAdmin(object):
    readonly_fields = ('wx_id', "date")
    list_display = ["mobile", "wx_id", "balance", "date"]
    search_fields = ('mobile',)
    list_filter = ('date',)


xadmin.site.register(Customer, CustomerAdmin)
