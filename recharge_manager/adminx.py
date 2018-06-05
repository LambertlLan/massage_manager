# __author: Lambert
# __date: 2018/5/18 11:14
# __author: Lambert

import xadmin
from .models import RechargeOrder, RechargeActive


def recharge_menu(obj):
    menus = [
        {
            'title': '充值记录',
            'perm': obj.get_model_perm(RechargeOrder, 'change'),
            'icon': 'fa fa-list-ul',
            'menus': (
                {'title': '充值记录', 'icon': 'fa fa-list-ul',
                 'url': obj.get_model_url(RechargeOrder, 'changelist')},
                {'title': '充值活动', 'icon': 'fa fa-gift',
                 'url': obj.get_model_url(RechargeActive, 'changelist')},
            )
        },

    ]
    return menus


class RechargeOrderAdmin(object):
    list_display = ["record_number", "user", "amount", "is_pay", "date"]
    search_fields = ('record_number', 'user__mobile')
    list_filter = ('is_pay',)
    ordering = ('-date',)


class RechargeActiveAdmin(object):
    list_display = ["desc", "recharge_amount", "present_amount"]


xadmin.site.register(RechargeOrder, RechargeOrderAdmin)
xadmin.site.register(RechargeActive, RechargeActiveAdmin)
