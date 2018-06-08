# Generated by Django 2.0.5 on 2018-05-23 17:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers_manager', '0002_remove_vouchers_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='vouchers',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='领取日期'),
            preserve_default=False,
        ),
    ]