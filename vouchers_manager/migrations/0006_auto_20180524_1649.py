# Generated by Django 2.0.5 on 2018-05-24 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers_manager', '0005_vouchersmanager_belong_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vouchers',
            name='voucher',
            field=models.ForeignKey(on_delete=None, to='vouchers_manager.VouchersManager', verbose_name='代金券分类'),
        ),
    ]
