# Generated by Django 4.1.2 on 2023-11-12 22:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0049_finalquizsresult_incorrect_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalquizsresult',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
