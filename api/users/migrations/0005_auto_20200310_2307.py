# Generated by Django 3.0.3 on 2020-03-10 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200310_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='a_birthdate',
        ),
        migrations.RemoveField(
            model_name='author',
            name='a_description',
        ),
        migrations.RemoveField(
            model_name='author',
            name='a_email',
        ),
        migrations.RemoveField(
            model_name='author',
            name='github',
        ),
        migrations.RemoveField(
            model_name='author',
            name='host',
        ),
        migrations.RemoveField(
            model_name='author',
            name='url',
        ),
    ]
