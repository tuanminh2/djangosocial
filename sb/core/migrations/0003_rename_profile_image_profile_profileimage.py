# Generated by Django 4.1.1 on 2022-10-31 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_id_user_profile_userid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profile_image',
            new_name='profileimage',
        ),
    ]