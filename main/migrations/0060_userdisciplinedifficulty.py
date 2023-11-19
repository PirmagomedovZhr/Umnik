# Generated by Django 4.1.2 on 2023-11-19 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0059_finalquizsresult_total_questions_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDisciplineDifficulty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty_block', models.CharField(choices=[('L1', 'Низкий 1'), ('L2', 'Низкий 2'), ('M1', 'Средний 1'), ('M2', 'Средний 2'), ('H1', 'Высокий 1'), ('H2', 'Высокий 2'), ('NN', 'Вводный')], default='NN', max_length=2, verbose_name='Блок сложности')),
                ('disciplin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.disciplin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
