# Generated by Django 4.1.1 on 2022-11-14 02:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_profile_image_profile_profileimage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 14, 9, 36, 2, 442433)),
        ),
    ]
