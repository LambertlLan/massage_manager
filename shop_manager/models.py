from django.db import models


# Create your models here.
class City(models.Model):
    city_name = models.CharField(max_length=64)

    def __str__(self):
        return f"城市:{self.city_name}"

    class Meta:
        verbose_name_plural = "城市管理"


class Shop(models.Model):
    shop_name = models.CharField(max_length=64, verbose_name="门店名称")
    area = models.CharField(max_length=64, verbose_name="所在区域")
    address = models.CharField(max_length=64, verbose_name="详细地址")
    image = models.ImageField(upload_to='upload', verbose_name="门店照片")
    city = models.ForeignKey("City", None, verbose_name="所属城市")
    program = models.ManyToManyField("MassageProgram", verbose_name="包含项目")

    def __str__(self):
        return f"门店:{self.shop_name}"

    class Meta:
        verbose_name_plural = "门店管理"


class SymptomCategory(models.Model):
    symptomName = models.CharField(max_length=32, verbose_name="症状名称")

    def __str__(self):
        return self.symptomName

    class Meta:
        verbose_name_plural = "症状分类"


class MassageProgram(models.Model):
    program_name = models.CharField(max_length=64, verbose_name="项目名称")
    suit_human = models.TextField(verbose_name="适宜人群")
    recuperate_method = models.TextField(verbose_name="调理方法")
    recuperate_flow = models.TextField(verbose_name="调理流程")
    maintain_method = models.TextField(verbose_name="自我保养方法")
    need_time = models.PositiveIntegerField(verbose_name="项目时间")
    program_shop = models.ForeignKey("SymptomCategory", None, verbose_name="选择分类")

    def __str__(self):
        return f"项目{self.program_name}"

    class Meta:
        verbose_name_plural = "按摩项目"


class Technician(models.Model):
    real_name = models.CharField(max_length=32, verbose_name="姓名")
    price = models.FloatField(verbose_name="价格/分钟")
    evaluate_grade = models.FloatField(verbose_name="评分")
    profile = models.TextField(verbose_name="个人简介")

    def __str__(self):
        return f"技师{self.real_name}"

    class Meta:
        verbose_name_plural = "调理师管理"
