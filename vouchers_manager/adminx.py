# __author: Lambert
# __date: 2018/5/18 10:55
# Register your models here.
import xadmin
from .models import Vouchers, VouchersManager

xadmin.site.register(Vouchers)
xadmin.site.register(VouchersManager)
