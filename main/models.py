from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    positions = (
        ('Преподаватель', 'Преподаватель'),
        ('Студент', 'Студент')
    )

    position = models.CharField('Должность', max_length=20, choices=positions, default='')


class Section(models.Model):
    # Определение модели данных для раздела
    title = models.CharField(max_length=100)

    def __str__(self):
        # Возвращение названия раздела в качестве строкового представления объекта
        return self.title

class Subsection(models.Model):
    # Определение модели данных для подраздела
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)

    def __str__(self):
        # Возвращение названия подраздела в качестве строкового представления объекта
        return self.title

