# Generated by Django 4.1.2 on 2023-11-15 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0055_finalquizsresult_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalquizsresult',
            name='grade',
            field=models.PositiveIntegerField(default=2, null=True),
        ),
    ]
