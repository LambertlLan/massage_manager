from django.db import models


# Create your models here.

class VouchersManager(models.Model):
    amount = models.FloatField(verbose_name="抵扣金额")
    use_shop = models.ManyToManyField('shop_manager.Shop', verbose_name="所属门店")
    effective_time = models.DateTimeField(verbose_name="有效期至")
    is_used = models.BooleanField(default=False, verbose_name="是否已经使用")

    def __str__(self):
        return f"代金券金额{self.amount}所属门店{self.use_shop}"

    class Meta:
        verbose_name_plural = "代金券管理"


class Vouchers(models.Model):
    voucher = models.ForeignKey("VouchersManager", None, verbose_name="所属代金券")
    is_used = models.BooleanField(default=False, verbose_name="是否已经使用")

    def __str__(self):
        return f"代金券分类id{self.voucher_id}是否已使用{self.is_used}"

    class Meta:
        verbose_name_plural = "用户代金券"
