# Generated by Django 4.1.2 on 2023-10-11 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_question_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('CH', 'Choice'), ('OP', 'Open')], default='CH', max_length=2, verbose_name='Тип вопроса'),
        ),
    ]
