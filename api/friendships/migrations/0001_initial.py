# Generated by Django 3.0.3 on 2020-03-10 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0004_auto_20200310_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_rec', to='users.Author')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_req', to='users.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friends', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends', to='users.Author')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='users.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_rec', to='users.Author')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_req', to='users.Author')),
            ],
        ),
    ]