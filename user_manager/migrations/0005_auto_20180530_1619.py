# Generated by Django 2.0.5 on 2018-05-30 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0004_auto_20180530_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='wx_id',
            field=models.CharField(default=None, max_length=64, null=True, verbose_name='微信OPENID'),
        ),
    ]
