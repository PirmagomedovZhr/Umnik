from .models import Groups, Disciplin, Topic, Question, Answer
from .models import User

# Предполагается, что у администратора установлены флаги is_staff и is_superuser
admin_user = User.objects.filter(is_staff=True, is_superuser=True).first()
def duplicate_discipline(original_discipline_name, new_group_name, new_discipline_name):
    # Создание новой группы
    new_group = Groups(name=new_group_name, user=admin_user)
    new_group.save()
    # Создание новой дисциплины
    new_discipline = Disciplin(name=new_discipline_name, groups=new_group, user=admin_user)
    new_discipline.save()

    # Копирование лекций (Topic)
    for topic in Topic.objects.filter(disciplin__name=original_discipline_name):
        topic.pk = None  # Сброс первичного ключа для создания нового экземпляра
        topic.disciplin = new_discipline
        topic.save()

    # Копирование вопросов и ответов
    for question in Question.objects.filter(disciplin__name=original_discipline_name):
        answers = list(question.answers.all())
        question.pk = None
        question.disciplin = new_discipline
        question.save()

        # Копирование ответов
        for answer in answers:
            answer.pk = None
            answer.question = question
            answer.save()
