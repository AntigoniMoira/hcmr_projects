# Generated by Django 2.0.5 on 2018-08-01 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_onlinedata'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='onlinedata',
            table='public"."hcmr_online_data_mv',
        ),
    ]