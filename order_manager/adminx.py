# __author: Lambert
# __date: 2018/5/18 11:14
# __author: Lambert

import xadmin
from .models import Order, ReservationRecord


def order_menu(obj):
    menus = [
        {
            'title': '订单管理',
            'perm': obj.get_model_perm(Order, 'change'),
            'icon': 'fa fa-first-order',
            'menus': (
                {'title': '订单列表', 'icon': 'fa fa-first-order',
                 'url': obj.get_model_url(Order, 'changelist')},
                {'title': '预约记录', 'icon': 'fa fa-list-alt',
                 'url': obj.get_model_url(ReservationRecord, 'changelist')},
            )
        },

    ]
    return menus


class OrderAdmin(object):
    # readonly_fields = ('user', 'order_number', 'date', 'complete')
    list_display = ["order_number", "user", "shop", "program", "technician",
                    "amount", "voucher", "pay_type_chinese", "complete", "date"]
    search_fields = ('order_number', 'user__mobile')
    list_filter = ('shop', 'program', 'technician', 'complete', 'date')
    ordering = ('-date',)
    list_editable = ['complete', ]
    style_fields = {'program': 'm2m_transfer', 'technician': 'm2m_transfer'}

    def pay_type_chinese(self, obj):
        if obj.pay_type == '0':
            return "余额支付"
        elif obj.pay_type == '1':
            return "微信支付"

    pay_type_chinese.short_description = "支付方式"


class ReservationRecordAdmin(object):
    # readonly_fields = ('user', 'order_number', 'date', 'complete')
    list_display = ["order", "order_user_mobile", "shop_name", "program", "technician", "start_time", "end_time",
                    "create_time"]
    search_fields = ('order__order_number', 'order__user__mobile')
    list_filter = ('create_time', 'program',)
    ordering = ('-create_time',)

    def shop_name(self, obj):
        return obj.order.shop.shop_name

    shop_name.short_description = "门店"

    def order_user_mobile(self, obj):
        return obj.order.user.mobile

    order_user_mobile.short_description = "用户手机号"


xadmin.site.register(Order, OrderAdmin)
xadmin.site.register(ReservationRecord, ReservationRecordAdmin)
