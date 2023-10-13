from django.db import models
from django.contrib.auth.models import AbstractUser


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
        ('', 'None'),
    )

    position = models.CharField('Должность', max_length=20, choices=positions, default='')
    difficulty_block = models.CharField('Блок сложности', max_length=2, choices=difficulty_blocks, default='', blank=True)


class Groups(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_groups')

class Disciplin(models.Model):
    name = models.CharField(max_length=100)
    groups = models.ForeignKey(Groups, on_delete=models.CASCADE)
    token = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



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


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('MC', 'Multiple Choice'),
        ('TF', 'Text Field'),
        # Добавьте другие типы по мере необходимости
    ]

    text = models.TextField('Текст вопроса')
    image = models.ImageField('Изображение вопроса', upload_to='question_images/', null=True, blank=True)
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

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct_answers_count = models.IntegerField('Количество правильных ответов')
    total_questions_count = models.IntegerField('Общее количество вопросов')
    # Другие необходимые поля
