# Generated by Django 5.2.2 on 2025-07-06 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix_app', '0003_alter_video_thumbnail_alter_video_video_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='genre',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='thumbnail',
            new_name='thumbnail_url',
        ),
    ]
