from django.db import models


# Create your models here.
class Customer(models.Model):
    mobile = models.CharField(max_length=32, verbose_name="手机号")
    wx_id = models.CharField(max_length=64, verbose_name="微信ID")
    balance = models.FloatField(verbose_name="余额")
    date = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    vouchers = models.ManyToManyField("vouchers_manager.Vouchers", verbose_name="代金券")

    def __str__(self):
        return f"用户id:{self.wx_id}"

    class Meta:
        verbose_name_plural = "用户管理"


class RechargeRecord(models.Model):
    user = models.ForeignKey("Customer", None, verbose_name="用户")
    amount = models.FloatField(verbose_name="充值金额")
    date = models.DateTimeField(auto_now_add=True, verbose_name="充值时间")

    def __str__(self):
        return f"用户{self.user_id}充值{self.amount}元"

    class Meta:
        verbose_name_plural = "充值记录"


class ExpendRecord(models.Model):
    user = models.ForeignKey("Customer", None, verbose_name="用户")
    shop = models.ForeignKey("shop_manager.Shop", None, verbose_name="消费门店")
    amount = models.FloatField(verbose_name="消费金额")
    date = models.DateTimeField(auto_now_add=True, verbose_name="消费时间")

    def __str__(self):
        return f"用户{self.user_id}充值{self.amount}元"

    class Meta:
        verbose_name_plural = "消费记录"
