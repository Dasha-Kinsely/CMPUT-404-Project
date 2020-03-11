# Generated by Django 3.0.3 on 2020-03-11 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200311_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='displayName',
            field=models.CharField(default='1', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='alias',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='users.Author'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='a_email',
            field=models.EmailField(max_length=60),
        ),
    ]
