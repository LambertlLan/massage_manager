from django.db import models
import os
from PIL import Image
from utils.compress_pictures import compress_picture


# Create your models here.
class City(models.Model):
    city_name = models.CharField(max_length=64, verbose_name="城市名称")

    def __str__(self):
        return f"{self.city_name}"

    class Meta:
        verbose_name_plural = "城市管理"


class Shop(models.Model):
    shop_name = models.CharField(max_length=64, verbose_name="门店名称")
    area = models.CharField(max_length=64, verbose_name="所在区域")
    address = models.CharField(max_length=64, verbose_name="详细地址")
    image = models.ImageField(upload_to='upload', verbose_name="门店照片", blank=True)
    city = models.ForeignKey("City", None, verbose_name="所属城市")
    program = models.ManyToManyField("MassageProgram", verbose_name="包含项目",blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="纬度")
    lng = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="经度")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Shop, self).save()

        compress_picture(self.image.path)

    def __str__(self):
        return self.shop_name

    class Meta:
        verbose_name_plural = "门店管理"


class SymptomCategory(models.Model):
    symptom_name = models.CharField(max_length=32, verbose_name="症状名称")
    symptom_english_name = models.CharField(max_length=32, verbose_name="症状英文名称")

    def __str__(self):
        return self.symptom_name

    class Meta:
        verbose_name_plural = "症状分类"


class MassageProgram(models.Model):
    program_name = models.CharField(max_length=64, verbose_name="项目名称")
    suit_human = models.TextField(verbose_name="适宜人群")
    recuperate_method = models.TextField(verbose_name="调理方法")
    recuperate_flow = models.TextField(verbose_name="调理流程")
    maintain_method = models.TextField(verbose_name="自我保养方法")
    need_time = models.PositiveIntegerField(verbose_name="项目时间(分钟)")
    image = models.ImageField(upload_to='upload', verbose_name="项目照片", blank=True)
    program_category = models.ForeignKey("SymptomCategory", None, verbose_name="所属分类")
    technician = models.ManyToManyField("Technician", verbose_name="调理师", blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(MassageProgram, self).save()

        compress_picture(self.image.path)

    def __str__(self):
        return self.program_name

    class Meta:
        verbose_name_plural = "按摩项目"


class Technician(models.Model):
    real_name = models.CharField(max_length=32, verbose_name="姓名")
    price = models.FloatField(verbose_name="价格/分钟")
    evaluate_grade = models.FloatField(verbose_name="评分")
    profile = models.TextField(verbose_name="个人简介")
    image = models.ImageField(upload_to='upload', verbose_name="技师照片", blank=True)
    belong_shop = models.ForeignKey("Shop", None, verbose_name="所属门店", default=None, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Technician, self).save()
        compress_picture(self.image.path)

    def __str__(self):
        return self.real_name

    class Meta:
        verbose_name_plural = "调理师管理"
