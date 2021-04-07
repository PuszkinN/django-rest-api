# Generated by Django 3.1.7 on 2021-04-04 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favorite_movies',
            field=models.ManyToManyField(blank=True, related_name='favorite_movies', to='content.Movie'),
        ),
        migrations.AddField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='followrequest',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='followrequest',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_sender', to=settings.AUTH_USER_MODEL),
        ),
    ]