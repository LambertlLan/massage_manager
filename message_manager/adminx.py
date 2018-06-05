# __author: Lambert
# __date: 2018/5/18 10:55
# Register your models here.
import xadmin
from .models import MessageCenter


def message_menu(obj):
    menus = [
        {
            'title': '消息管理',
            'perm': obj.get_model_perm(MessageCenter, 'change'),
            'icon': 'fa fa-comments',
            'menus': (
                {'title': '消息列表', 'icon': 'fa fa-comments',
                 'url': obj.get_model_url(MessageCenter, 'changelist')},

            )
        }
    ]
    return menus


class MessageCenterAdmin(object):
    list_display = ['user', 'content', 'date']
    search_fields = ['user__mobile', ]
    list_filter = ['date', ]
    ordering = ('-date',)


xadmin.site.register(MessageCenter, MessageCenterAdmin)
