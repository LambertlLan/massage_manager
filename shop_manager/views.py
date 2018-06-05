from django.shortcuts import render
from django.http import JsonResponse
from user_manager.views import Base
from shop_manager import models as shop_models
from order_manager.models import ReservationRecord
from django.db.models import Q
import datetime
import time


# Create your views here.
class ShopList(Base):
    """获取门店数据"""

    def get(self, request):
        city_id = request.GET.get("city_id")
        shop_list = shop_models.Shop.objects.filter(id=city_id).values()
        shop_list = list(shop_list)
        self.res_json["results"] = {"shopList": shop_list}
        return JsonResponse(self.res_json)


class SymptomList(Base):
    """查询四个项目分类对应的项目列表"""

    def get(self, request):
        shop_id = request.GET.get("shop_id")
        """根据门店id查项目"""

        symptom_category = shop_models.SymptomCategory.objects.all().values("id", "symptom_english_name")
        symptom_category = list(symptom_category)
        result = {}
        for item in symptom_category:
            result[item["symptom_english_name"]] = list(shop_models.Shop.objects.get(id=shop_id).program.filter(
                program_category=item["id"]).values("id", "program_name", "need_time", "suit_human", "image"))
        self.res_json["results"] = result
        return JsonResponse(self.res_json)


class SymptomInfo(Base):
    """项目详情"""

    def get(self, request):
        pro_id = request.GET.get("pro_id")
        results = shop_models.MassageProgram.objects.filter(id=pro_id).values("suit_human", "recuperate_method",
                                                                              "recuperate_flow", "maintain_method",
                                                                              "image")
        results = list(results)[0]

        self.res_json["results"] = results
        return JsonResponse(self.res_json)


class CityList(Base):
    """城市列表"""

    def get(self, request):
        city_list = shop_models.City.objects.all().values()
        city_list = list(city_list)
        self.res_json["results"] = {"cityList": city_list}
        return JsonResponse(self.res_json)


class TechnicianList(Base):
    """技师列表"""

    # SELECT * FROM test_table
    # WHERE
    # (start_time >= a AND start_time <= b)
    # OR (start_time <= a AND end_time >= b)
    # OR (end_time >= a AND end_time <= b)
    def get(self, request):
        shop_id = request.GET.get("shop_id")
        program_id = request.GET.get("program_id")
        _start_time = request.GET.get("start_time")
        _end_time = request.GET.get("end_time")
        try:
            time.strptime(_start_time, "%Y-%m-%d %H:%M")
            time.strptime(_end_time, "%Y-%m-%d %H:%M")
        except Exception as e:
            self.res_json["code"] = 1
            self.res_json["msg"] = "当前日期无效"
            return JsonResponse(self.res_json)
        # 该店该项目下的技师
        technician_list = shop_models.MassageProgram.objects.get(id=program_id).technician.filter(
            belong_shop_id=shop_id).values()

        # 根据技师id去查预约列表,看时间是否重叠
        results = []
        now = datetime.datetime.now()
        delta = datetime.timedelta(minutes=3)
        n_minutes = now - delta
        three_minutes = n_minutes.strftime('%Y-%m-%d %H:%M:%S')
        for item in technician_list:
            record_number = ReservationRecord.objects.filter(Q(start_time__range=(_start_time, _end_time)) | Q(
                end_time__range=(_start_time, _end_time)) | Q(start_time__lte=_start_time, end_time__gte=_end_time),
                                                             technician_id=item["id"])
            """查询符合条件的预约记录已支付的数量和未支付但是创建时间在三分钟之内的数量
               如果两个条件都为0说明该技师该时间段内无预约记录
               主要用于微信支付未付款的情况"""
            if record_number.filter(order__is_pay=True, order__complete=False).count() == 0 and record_number.filter(
                    order__is_pay=False, order__date__gt=three_minutes, order__complete=False).count() == 0:
                results.append(item)

        self.res_json["results"] = {"technician_list": results}
        return JsonResponse(self.res_json)
