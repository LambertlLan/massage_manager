from django.db import models


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey("user_manager.Customer", None, verbose_name="用户")
    order_number = models.CharField(max_length=64, verbose_name="订单编号")
    shop = models.ForeignKey("shop_manager.Shop", None, verbose_name="预约门店")
    program = models.ManyToManyField("shop_manager.MassageProgram", verbose_name="项目", blank=True)
    technician = models.ManyToManyField("shop_manager.Technician", verbose_name="理疗师", blank=True)
    complete = models.BooleanField(default=False, verbose_name="是否完成")
    amount = models.FloatField(verbose_name="订单金额")
    voucher = models.ForeignKey("vouchers_manager.Vouchers", None, null=True, default=None, verbose_name="使用代金券")
    need_pay = models.FloatField(default=0, verbose_name="支付金额")
    pay_type = models.CharField(max_length=32, default='0', verbose_name="充值方式(0=余额,1=微信)")
    is_pay = models.BooleanField(default=False, verbose_name="是否支付")
    date = models.DateTimeField(auto_now_add=True, verbose_name="下单时间")

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name_plural = "订单"


class ReservationRecord(models.Model):
    order = models.ForeignKey("Order", None, verbose_name="订单编号")
    program = models.ForeignKey("shop_manager.MassageProgram", None, verbose_name="项目")
    technician = models.ForeignKey("shop_manager.Technician", None, verbose_name="理疗师")
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return str(self.order.id)

    class Meta:
        verbose_name_plural = "预约记录"
