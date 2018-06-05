# __author: Lambert
# __date: 2018/5/18 10:55
# Register your models here.
import xadmin
from .models import City, Shop, SymptomCategory, MassageProgram, Technician


def shop_menu(obj):
    menus = [
        {
            'title': '门店管理',
            'perm': obj.get_model_perm(Shop, 'change'),
            'icon': 'fa fa-building',
            'menus': (
                {'title': '门店列表', 'icon': 'fa fa-home',
                 'url': obj.get_model_url(Shop, 'changelist')},
                {'title': '项目列表', 'icon': 'fa fa-briefcase',
                 'url': obj.get_model_url(MassageProgram, 'changelist')},
                {'title': '调理师列表', 'icon': 'fa fa-male',
                 'url': obj.get_model_url(Technician, 'changelist')},
                {'title': '症状分类列表', 'icon': 'fa fa-archive',
                 'url': obj.get_model_url(SymptomCategory, 'changelist')},
                {'title': '城市列表', 'icon': 'fa fa-hospital-o',
                 'url': obj.get_model_url(City, 'changelist')},
                {
                    'title': '经纬度拾取器',
                    'icon': 'fa fa-location-arrow ',
                    'url': "/mini-manager/map",
                },

            )
        }
    ]
    return menus


class CityAdmin(object):
    list_display = ["id", "city_name"]
    list_editable = ["city_name"]


class ShopAdmin(object):
    list_display = ["shop_name", "city", "area", "lat", "lng", "address"]
    search_fields = ('shop_name',)
    list_filter = ('city', 'area')
    style_fields = {'technician': 'm2m_transfer', 'program': 'm2m_transfer'}


class MassageProgramAdmin(object):
    list_display = ["program_name", "need_time", "program_category", "technician"]
    search_fields = ('program_name',)
    list_filter = ('program_category',)
    style_fields = {'technician': 'm2m_transfer'}
    # 自定义字段
    # def technician_real_name(self, obj):
    #     return [i.real_name for i in obj.technician.all()]

    # technician_real_name.short_description = "调理师"


class TechnicianAdmin(object):
    list_display = ["real_name", "belong_shop", "price", "evaluate_grade", "profile"]
    search_fields = ('real_name',)
    list_filter = ('evaluate_grade', 'belong_shop')


class SymptomCategoryAdmin(object):
    list_display = ["symptom_name", "symptom_english_name"]


xadmin.site.register(City, CityAdmin)
xadmin.site.register(Shop, ShopAdmin)
xadmin.site.register(SymptomCategory, SymptomCategoryAdmin)
xadmin.site.register(MassageProgram, MassageProgramAdmin)
xadmin.site.register(Technician, TechnicianAdmin)
