# Generated by Django 4.1.1 on 2022-11-01 09:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_likepost_alter_post_create_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowersCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=500)),
                ('userName', models.CharField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 1, 16, 35, 24, 7726)),
        ),
    ]
