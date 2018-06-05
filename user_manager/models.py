from django.db import models


# Create your models here.
class Customer(models.Model):
    mobile = models.CharField(max_length=32, verbose_name="手机号", default=None, null=True, blank=True)
    wx_id = models.CharField(max_length=64, verbose_name="微信OPENID", default=None, null=True)
    balance = models.FloatField(verbose_name="余额", default=0.00)
    date = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    def __str__(self):
        return str(self.mobile)

    class Meta:
        verbose_name_plural = "用户管理"


class MsgCode(models.Model):
    mobile = models.CharField(max_length=32, verbose_name="获取验证码手机号")
    msg_code = models.PositiveIntegerField(verbose_name="验证码")
    create_time = models.DateTimeField(verbose_name="验证码创建时间", auto_now=True)

    def __str__(self):
        return self.msg_code

    class Meta:
        verbose_name_plural = "验证码表"
