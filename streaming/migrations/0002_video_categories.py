# Generated by Django 5.1.1 on 2024-09-29 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='categories',
            field=models.ManyToManyField(related_name='videos', to='streaming.category'),
        ),
    ]