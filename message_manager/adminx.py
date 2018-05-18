# __author: Lambert
# __date: 2018/5/18 10:55
# Register your models here.
import xadmin
from .models import MessageCenter


class MessageCenterAdmin(object):
    list_display = ['content', 'date']
    search_fields = ['content', ]
    list_filter = ['date', ]
    model_icon = 'fa fa-comments'


xadmin.site.register(MessageCenter, MessageCenterAdmin)
