# Generated by Django 4.1.2 on 2023-10-11 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_question_correct_answer_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='correct_answer_text',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_type',
        ),
    ]
