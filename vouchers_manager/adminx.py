# __author: Lambert
# __date: 2018/5/18 10:55
# Register your models here.
import xadmin
from .models import Vouchers, VouchersManager


def vouchers_menu(obj):
    menus = [
        {
            'title': '代金券管理',
            'perm': obj.get_model_perm(Vouchers, 'change'),
            'icon': 'fa fa-credit-card-alt',
            'menus': (
                {'title': '代金券分类', 'icon': 'fa fa-credit-card',
                 'url': obj.get_model_url(VouchersManager, 'changelist')},
                {'title': '用户代金券', 'icon': 'fa fa-shopping-bag',
                 'url': obj.get_model_url(Vouchers, 'changelist')},

            )
        }
    ]
    return menus


class VouchersAdmin(object):
    list_display = ["user", "voucher", "is_used", "belong_shop"]
    readonly_fields = ('is_used',)
    search_fields = ('user__mobile',)
    list_filter = ("date", "voucher")

    def belong_shop(self, obj):
        return [i.shop_name for i in obj.voucher.belong_shop.all()]

    belong_shop.short_description = "所属门店"


class VouchersManagerAdmin(object):
    list_display = ["id", "amount", "belong_shop", "effective_time", "is_issue"]
    search_fields = ('belong_shop__shop_name',)
    list_filter = ("effective_time", "belong_shop",)
    style_fields = {'belong_shop': 'm2m_transfer'}
    list_editable = ["is_issue"]


xadmin.site.register(Vouchers, VouchersAdmin)
xadmin.site.register(VouchersManager, VouchersManagerAdmin)
