# Generated by Django 4.1.2 on 2023-11-19 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0057_finalquizsresult_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizresult',
            name='difficulty_block_after_test',
            field=models.CharField(default=12, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quizresult',
            name='difficulty_block_before_test',
            field=models.CharField(default=123, max_length=50),
            preserve_default=False,
        ),
    ]
