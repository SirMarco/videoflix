# Generated by Django 5.1.1 on 2024-10-15 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0011_video_progress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='progress',
        ),
    ]