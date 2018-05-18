from django.db import models


# Create your models here.
# 消息中心
class MessageCenter(models.Model):
    user = models.ForeignKey("user_manager.Customer", None, verbose_name="所属用户")
    content = models.TextField(verbose_name="消息内容")
    date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return f"消息编号{self.id}"

    class Meta:
        verbose_name_plural = "消息管理"
