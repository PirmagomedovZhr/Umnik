from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    positions = (
        ('Преподаватель', 'Преподаватель'),
        ('Студент', 'Студент')
    )

    difficulty_blocks = (
        ('L1', 'Низкий 1'),
        ('L2', 'Низкий 2'),
        ('M1', 'Средний 1'),
        ('M2', 'Средний 2'),
        ('H1', 'Высокий 1'),
        ('H2', 'Высокий 2'),
        ('NN', 'Вводный'),
    )

    position = models.CharField('Должность', max_length=20, choices=positions, default='')
    difficulty_block = models.CharField('Блок сложности', max_length=2, choices=difficulty_blocks, default='Вводный', blank=True)
    disciplines = models.ManyToManyField('Disciplin', related_name='users', blank=True)


class Groups(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_groups')

    def __str__(self):
        return self.name


class Disciplin(models.Model):
    name = models.CharField(max_length=100)
    groups = models.ForeignKey(Groups, on_delete=models.CASCADE)
    token = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='discipline_images/', null=True, blank=True)  # новое поле для изображения

    def get_absolute_url(self):
        return reverse('disciplin_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Topic(models.Model):
    title = models.CharField('Название', max_length=100)
    content = models.TextField('Текст', blank=True)
    disciplin = models.ForeignKey(Disciplin, on_delete=models.CASCADE, related_name='topics')
    video_url = models.URLField('Ссылка на видео', blank=True)
    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('MC', 'Ответы с галочкой'),
        ('TF', 'Текстовый ответ'),

    ]

    text = models.TextField('Текст вопроса')
    image = models.ImageField('Изображение', upload_to='question_images/', null=True, blank=True)
    difficulty_block = models.CharField('Блок сложности', max_length=2, choices=User.difficulty_blocks, blank=True,
                                        null=True)
    question_type = models.CharField('Тип вопроса', max_length=2, choices=QUESTION_TYPE_CHOICES, default='MC')
    disciplin = models.ForeignKey(Disciplin, on_delete=models.CASCADE, related_name='questions')


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField('Текст ответа', blank=True,
                            null=True)  # Текст может быть пустым для вопросов с текстовым полем
    is_correct = models.BooleanField('Правильный ответ', default=False)

    # Другие необходимые поля

    def __str__(self):
        return self.text




class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disciplin = models.ForeignKey(Disciplin, on_delete=models.CASCADE)
    correct_answers_count = models.PositiveIntegerField()
    percentage = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)



class FinalQuizsResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disciplin = models.ForeignKey(Disciplin, on_delete=models.CASCADE)  # добавьте эту строку
    correct_answers_count = models.PositiveIntegerField()
    percentage = models.FloatField()
    grade = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
