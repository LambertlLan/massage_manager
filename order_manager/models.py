from django.db import models


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey("user_manager.Customer", None, verbose_name="用户")
    order_number = models.CharField(max_length=64, verbose_name="订单编号")
    shop = models.ForeignKey("shop_manager.Shop", None, verbose_name="预约门店")
    program = models.ForeignKey("shop_manager.MassageProgram", None, verbose_name="项目")
    technician = models.ForeignKey("shop_manager.Technician", None, verbose_name="理疗师")
    complete = models.BooleanField(default=False, verbose_name="是否完成")
    amount = models.FloatField(verbose_name="订单金额")
    voucher = models.ForeignKey("vouchers_manager.Vouchers", None, verbose_name="使用代金券")
    date = models.DateTimeField(auto_now_add=True, verbose_name="下单时间")

    def __str__(self):
        return f"订单编号{self.order_number}金额{self.amount}"

    class Meta:
        verbose_name_plural = "订单管理"
