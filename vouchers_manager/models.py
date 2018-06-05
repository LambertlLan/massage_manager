from django.db import models


# Create your models here.

class VouchersManager(models.Model):
    amount = models.FloatField(verbose_name="抵扣金额")
    belong_shop = models.ManyToManyField('shop_manager.Shop', verbose_name="所属门店", blank=True)
    is_issue = models.BooleanField(default=False, verbose_name='是否发放(如果勾选多个,默认发放ID最大的)')
    effective_time = models.DateTimeField(verbose_name="有效期至")

    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name_plural = "代金券管理"


class Vouchers(models.Model):
    user = models.ForeignKey("user_manager.Customer", None, verbose_name="所属用户")
    voucher = models.ForeignKey("VouchersManager", None, verbose_name="代金券分类")
    is_used = models.BooleanField(default=False, verbose_name="是否已经使用")
    date = models.DateTimeField(auto_now_add=True, verbose_name="领取日期")

    def __str__(self):
        return str(self.voucher.amount)

    class Meta:
        verbose_name_plural = "用户代金券"
