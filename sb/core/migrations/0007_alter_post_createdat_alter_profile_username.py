# Generated by Django 4.1.1 on 2022-11-14 03:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_post_createdat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 14, 10, 33, 16, 965795)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='userName',
            field=models.CharField(default='usernamedefaut', max_length=100, unique=True),
        ),
    ]