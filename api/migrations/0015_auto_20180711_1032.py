# Generated by Django 2.0.5 on 2018-07-11 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20180710_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='userPhone',
            field=models.CharField(max_length=30),
        ),
    ]
