# Generated by Django 4.1.2 on 2023-11-19 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0058_quizresult_difficulty_block_after_test_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalquizsresult',
            name='total_questions_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
