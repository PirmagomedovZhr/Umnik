# Generated by Django 4.1.2 on 2023-11-26 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0062_alter_user_group_for_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_exam_in_progress',
            field=models.BooleanField(default=False),
        ),
    ]
