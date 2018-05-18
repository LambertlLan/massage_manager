# __author: Lambert
# __date: 2018/5/18 10:28

import xadmin
from xadmin import views


class GlobalSetting(object):
    # 设置base_site.html的Title
    site_title = '浴足后台'
    # 设置base_site.html的Footer
    site_footer = '浴足后台管理系统'
    # 设置折叠菜单
    menu_style = "accordion"


xadmin.site.register(views.CommAdminView, GlobalSetting)
