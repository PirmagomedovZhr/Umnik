# Generated by Django 4.1.2 on 2023-10-09 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_remove_test_block_remove_test_is_final_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answers_count', models.IntegerField(verbose_name='Количество правильных ответов')),
                ('total_questions_count', models.IntegerField(verbose_name='Общее количество вопросов')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='usertestresult',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='usertestresult',
            name='test',
        ),
        migrations.RemoveField(
            model_name='usertestresult',
            name='user',
        ),
        migrations.RemoveField(
            model_name='question',
            name='test',
        ),
        migrations.AddField(
            model_name='user',
            name='difficulty_block',
            field=models.CharField(blank=True, choices=[('L1', 'Низкий 1'), ('L2', 'Низкий 2'), ('M1', 'Средний 1'), ('M2', 'Средний 2'), ('H1', 'Высокий 1'), ('H2', 'Высокий 2'), ('', 'None')], default='', max_length=2, verbose_name='Блок сложности'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False, verbose_name='Правильный ответ'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(verbose_name='Текст ответа'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(verbose_name='Текст вопроса'),
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.DeleteModel(
            name='UserTestResult',
        ),
        migrations.AddField(
            model_name='testresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
