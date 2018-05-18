# __author: Lambert
# __date: 2018/5/18 10:55
# Register your models here.

import xadmin
from .models import Customer, RechargeRecord, ExpendRecord

from xadmin import views


class GlobalSetting(object):
    # 设置base_site.html的Title
    site_title = 'MASSAGE MANAGER'
    # 设置base_site.html的Footer
    site_footer = 'MASSAGE后台管理系统'
    # 设置折叠菜单
    menu_style = "accordion"


class BaseSetting(object):
    enable_themes = True  # 打开主题功能
    use_bootswatch = True  #


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
# xadmin全局配置结束


xadmin.site.register(Customer)
xadmin.site.register(RechargeRecord)
xadmin.site.register(ExpendRecord)
