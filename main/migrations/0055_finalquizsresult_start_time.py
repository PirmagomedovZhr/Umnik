# Generated by Django 4.1.2 on 2023-11-15 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_user_exam_attempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalquizsresult',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
