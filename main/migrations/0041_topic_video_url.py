# Generated by Django 4.1.2 on 2023-11-01 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_finalquizsresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='video_url',
            field=models.URLField(blank=True, verbose_name='Ссылка на видео'),
        ),
    ]
