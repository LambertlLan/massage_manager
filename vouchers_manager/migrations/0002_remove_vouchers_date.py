# Generated by Django 2.0.5 on 2018-05-23 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers_manager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vouchers',
            name='date',
        ),
    ]
