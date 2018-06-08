# Generated by Django 2.0.5 on 2018-05-30 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recharge_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RechargeActive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recharge_amount', models.FloatField(verbose_name='金额')),
                ('desc', models.CharField(max_length=64, verbose_name='标题')),
                ('present_amount', models.FloatField(verbose_name='赠送金额')),
            ],
            options={
                'verbose_name_plural': '充值活动',
            },
        ),
    ]