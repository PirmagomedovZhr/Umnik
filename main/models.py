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


class Test(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # Можно добавить другие необходимые поля


class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)


class UserTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField()

    # Если нужно, добавьте дату прохождения или другие связанные поля

    class Meta:
        unique_together = ('user', 'test')