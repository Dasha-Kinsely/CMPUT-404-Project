# Generated by Django 3.0.3 on 2020-03-15 00:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.TextField(choices=[('author', 'Author'), ('admin', 'Admin')], default='author', max_length=10)),
                ('approved', models.BooleanField(default=False)),
                ('avatar', models.ImageField(blank=True, upload_to='uploads')),
                ('github', models.URLField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
