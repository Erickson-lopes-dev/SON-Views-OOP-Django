# Generated by Django 3.0.6 on 2020-07-10 16:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Adress',
            new_name='Address',
        ),
    ]