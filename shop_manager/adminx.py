# __author: Lambert
# __date: 2018/5/18 10:55
# Register your models here.
import xadmin
from .models import City, Shop, SymptomCategory, MassageProgram, Technician


class CityAdmin(object):
    list_display = ["city_name"]


xadmin.site.register(City, CityAdmin)
xadmin.site.register(Shop)
xadmin.site.register(SymptomCategory)
xadmin.site.register(MassageProgram)
xadmin.site.register(Technician)
