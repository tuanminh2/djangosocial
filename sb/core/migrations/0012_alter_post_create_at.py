# Generated by Django 4.0.7 on 2022-11-03 04:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_post_create_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 3, 11, 43, 1, 381290)),
        ),
    ]
