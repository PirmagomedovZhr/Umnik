# Generated by Django 4.1.2 on 2023-11-01 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_alter_question_difficulty_block_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinalQuizsResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answers_count', models.PositiveIntegerField()),
                ('percentage', models.FloatField()),
                ('grade', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('disciplin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.disciplin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
