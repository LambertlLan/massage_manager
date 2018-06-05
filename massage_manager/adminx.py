# __author: Lambert
# __date: 2018/5/22 16:44

import xadmin

from xadmin import views

# menus
from user_manager.adminx import user_menu
from order_manager.adminx import order_menu


class GlobalSetting(object):
    # 设置base_site.html的Title
    site_title = 'MASSAGE MANAGER'
    # 设置base_site.html的Footer
    site_footer = 'MASSAGE后台管理系统'
    # 设置折叠菜单
    menu_style = "accordion"

    def get_site_menu(self):
        menus = []
        menus.extend(user_menu(self))
        menus.extend(order_menu(self))

        return menus


class BaseSetting(object):
    enable_themes = True  # 打开主题功能
    use_bootswatch = True  #


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
