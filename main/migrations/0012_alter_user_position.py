# Generated by Django 4.1.2 on 2023-09-17 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_project_is_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(choices=[('Архитектор', 'архитектор'), ('Конструктор', 'конструктор'), ('Дизайнер', 'дизайнер')], default='', max_length=12, verbose_name='Должность'),
        ),
    ]
