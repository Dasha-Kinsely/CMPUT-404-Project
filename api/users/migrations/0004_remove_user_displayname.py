# Generated by Django 3.0.3 on 2020-03-27 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200327_0706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='displayName',
        ),
    ]