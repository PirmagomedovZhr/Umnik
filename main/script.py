from .models import Groups, Disciplin, Topic, Question, Answer
from .models import User

# Предполагается, что у администратора установлены флаги is_staff и is_superuser
admin_user = User.objects.filter(is_staff=True, is_superuser=True).first()
def copy_questions(source_discipline_name, target_discipline_name):
    source_discipline = Disciplin.objects.get(name=source_discipline_name)
    target_discipline = Disciplin.objects.get(name=target_discipline_name)

    for block in User.difficulty_blocks:
        # Получение по 5 вопросов каждого блока сложности
        questions = Question.objects.filter(disciplin=source_discipline, difficulty_block=block[0])[:10]
        for topic in Topic.objects.filter(disciplin__name=source_discipline):
            topic.pk = None  # Сброс первичного ключа для создания нового экземпляра
            topic.disciplin = target_discipline
            topic.save()

        for question in questions:
            # Копирование вопросов
            answers = list(question.answers.all())
            question.pk = None
            question.disciplin = target_discipline
            question.save()

            # Копирование ответов
            for answer in answers:
                answer.pk = None
                answer.question = question
                answer.save()
