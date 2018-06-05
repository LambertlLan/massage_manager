from django.db import models


class RechargeOrder(models.Model):
    user = models.ForeignKey("user_manager.Customer", None, verbose_name="用户")
    amount = models.FloatField(verbose_name="充值金额")
    record_number = models.CharField(max_length=64, verbose_name="充值订单号")
    is_pay = models.BooleanField(default=False, verbose_name="支付状态")
    date = models.DateTimeField(auto_now_add=True, verbose_name="充值日期")

    def __str__(self):
        return "%s %s" % (self.user, self.amount)

    class Meta:
        verbose_name_plural = "充值订单"


class RechargeActive(models.Model):
    desc = models.CharField(max_length=64, verbose_name="标题")
    recharge_amount = models.FloatField(verbose_name="充值金额")
    present_amount = models.FloatField(verbose_name="赠送金额")

    def __str__(self):
        return str(self.recharge_amount)

    class Meta:
        verbose_name_plural = "充值活动"
