# Generated by Django 2.0.5 on 2018-05-23 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_manager', '0001_initial'),
        ('vouchers_manager', '0004_remove_vouchersmanager_use_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='vouchersmanager',
            name='belong_shop',
            field=models.ManyToManyField(to='shop_manager.Shop', verbose_name='所属门店'),
        ),
    ]
