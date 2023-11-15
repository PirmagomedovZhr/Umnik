from django.http import HttpResponseRedirect, HttpResponseForbidden
from .forms import SignUpForm, SignInForm, QuizForm, GroupForm, DisciplineForm, TokenForm, TopicForm
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Disciplin, Topic
from django.shortcuts import render, redirect
from .forms import QuestionForm, AnswerForm
from .models import Question
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
from functools import wraps

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.position == 'Преподаватель':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('base')  # Замените 'base' на URL вашей базовой страницы
    return _wrapped_view


def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.position == 'Студент':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('base')  # Замените 'base' на URL вашей базовой страницы
    return _wrapped_view

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return render(request, 'main/admin/base.html')
            else:
                return render(request, 'main/users/base.html')
        else:
            return render(request, 'main/signup.html', context={
                'form': SignUpForm(),
        })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main/signin.html', context={
                'form': form,
            })
        return render(request, 'main/signup.html', context={
            'form': form,
        })


class SignInView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return render(request, 'main/admin/base.html')
            else:
                return render(request, 'main/users/base.html')
        else:
            form = SignInForm()
            return render(request, 'main/signin.html', context={
                'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'main/signin.html', context={
            'form': form,
        })


class LadderView(View):
    template_name = 'main/users/ladder.html'

    def get(self, request, disciplin_id):
        if request.user.is_authenticated and request.user.position == 'Студент':
            final_quiz_in_progress = FinalQuizsResult.objects.filter(
                user=request.user,
                disciplin=Disciplin.objects.get(id=disciplin_id),
                is_completed=False
            ).exists()

            return render(request, self.template_name, {
                'disciplin_id': disciplin_id,
                'final_quiz_in_progress': final_quiz_in_progress
            })
        else:
            return HttpResponseRedirect('/signin')

    def post(self, request, disciplin_id):
        if request.user.is_authenticated and request.user.position == 'Студент':
            return redirect('base')  # Пример перенаправления на базовую страницу
        else:
            return HttpResponseRedirect('/signin')




class DisciplinView(View):
    template_name = 'main/users/disciplin.html'

    def get(self, request):
        if request.user.is_authenticated and request.user.position == 'Студент':
            form = TokenForm()
            user_disciplines = request.user.disciplines.all()
            return render(request, self.template_name, {'form': form, 'user_disciplines': user_disciplines})
        else:
            return HttpResponseRedirect('/signin')

    def post(self, request):
        if request.user.is_authenticated and request.user.position == 'Студент':
            form = TokenForm(request.POST)
            if form.is_valid():
                token = form.cleaned_data['token']
                try:
                    discipline = Disciplin.objects.get(token=token)
                    request.user.disciplines.add(discipline)
                except Disciplin.DoesNotExist:
                    pass  # обработка случая, когда дисциплины с таким токеном не существует
                return redirect('disciplin')
            else:
                # Обработка невалидной формы
                pass
        else:
            return HttpResponseRedirect('/signin')



@student_required
def topic_detail(request, topic_id):  # Переименовано для ясности
    topic = Topic.objects.get(id=topic_id)  # Изменено здесь
    return render(request, 'main/users/topic_detail.html', {'topic': topic})  # Изменено здесь


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect('signin')

@student_required
def quiz_view(request, disciplin_id):
    disciplin = get_object_or_404(Disciplin, id=disciplin_id)

    if request.user.difficulty_block:
        questions = Question.objects.filter(difficulty_block=request.user.difficulty_block, disciplin=disciplin)
    else:
        questions = Question.objects.filter(difficulty_block__isnull=True, disciplin=disciplin)

    if request.method == 'POST':
        print(request.POST)
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            correct_answers_count = 0
            incorrect_answers = []

            for question, answer_text_or_instance in zip(questions, form.cleaned_data.values()):
                is_correct = False
                if question.question_type == 'MC':
                    correct_answers = set(question.answers.filter(is_correct=True).values_list('id', flat=True))
                    user_answers = set([answer.id for answer in answer_text_or_instance])
                    is_correct = correct_answers == user_answers
                    correct_answers_count += 1 if is_correct else 0
                elif question.question_type == 'TF':
                    correct_answer = question.answers.filter(is_correct=True).first()
                    if correct_answer and correct_answer.text.strip().lower() == answer_text_or_instance.strip().lower():
                        is_correct = True
                        correct_answers_count += 1

                if not is_correct:
                    incorrect_answers.append({
                        'question_id': question.id,
                        'user_answer': str(answer_text_or_instance)  # Пример сохранения текстового ответа пользователя
                    })

            percentage = (correct_answers_count / len(questions)) * 100
            new_block = 'NN'
            if request.user.difficulty_block == 'NN':
                new_block = 'H1' if percentage >= 95 else 'M1' if percentage >= 70 else 'L1'
            elif request.user.difficulty_block == 'L1':
                new_block = 'L2' if percentage >= 70 else 'L1'
            elif request.user.difficulty_block == 'L2':
                new_block = 'M1' if percentage > 80 else 'L2' if percentage >= 70 else 'L1'
            elif request.user.difficulty_block == 'M1':
                new_block = 'M2' if percentage > 80 else 'M1' if percentage >= 70 else 'L2'
            elif request.user.difficulty_block == 'M2':
                new_block = 'H1' if percentage > 80 else 'M2' if percentage >= 70 else 'M1'
            elif request.user.difficulty_block == 'H1':
                new_block = 'H2' if percentage > 80 else 'H1' if percentage >= 70 else 'M2'
            elif request.user.difficulty_block == 'H2':
                new_block = 'H2' if percentage > 90 else 'H1'

            request.user.difficulty_block = new_block
            request.user.save()

            request.session['result_data'] = {
                'correct_answers_count': correct_answers_count,
                'percentage': percentage,
                'new_block': new_block
            }

            quiz_result = QuizResult(
                user=request.user,
                disciplin=disciplin,
                correct_answers_count=correct_answers_count,
                percentage=percentage,
                incorrect_answers=incorrect_answers
            )
            quiz_result.save()

            return redirect('disciplin')

    else:
        form = QuizForm(questions=questions)

    return render(request, 'main/users/quiz.html', {'questions_and_forms': zip(questions, form), 'disciplin_id': disciplin_id})





from .models import QuizResult
@student_required
def discipline_results_view(request, disciplin_id):
    disciplin = Disciplin.objects.get(id=disciplin_id)
    results = QuizResult.objects.filter(user=request.user, disciplin=disciplin)

    return render(request, 'main/users/discipline_results.html', {'disciplin': disciplin, 'results': results})


def final_quiz_results_view(request, disciplin_id):
    disciplin = Disciplin.objects.get(id=disciplin_id)
    results = FinalQuizsResult.objects.filter(user=request.user, disciplin=disciplin)

    # Получите наивысшую оценку, если результаты есть
    max_grade = None
    if results.exists():
        max_grade = max(result.grade for result in results)

    return render(request, 'main/users/final_quiz_results.html',
                  {'disciplin': disciplin, 'results': results, 'max_grade': max_grade})


def result_view(request):
    if request.user.is_authenticated:
        if request.user.position == 'Преподаватель':
            template = 'main/admin/base.html'
        else:
            template = 'main/users/base.html'
        return render(request, template)
    else:
        return HttpResponseRedirect('/signin')



@teacher_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
            return redirect('homesss')
    else:
        form = GroupForm()

    if request.user.position == 'Преподаватель':
        template_name = 'main/admin/create_group.html'
        context = {'form': form}
    elif request.user.position == 'Студент':
        template_name = 'main/users/base.html'
        topics = Topic.objects.all()
        user_disciplines = request.user.disciplines.all()
        context = {'form': form, 'topics': topics, 'user_disciplines': user_disciplines}
    else:
        return HttpResponseForbidden("У вас нет прав доступа к этой странице.")

    return render(request, template_name, context)



@teacher_required
def create_discipline(request):
    if request.method == 'POST':
        form = DisciplineForm(request.POST, request.FILES, user=request.user)  # Изменение здесь
        if form.is_valid():
            discipline = form.save(commit=False)
            discipline.user = request.user
            discipline.save()
            return redirect('homesss')
    else:
        form = DisciplineForm(user=request.user)
    return render(request, 'main/admin/create_discipline.html', {'form': form})



@teacher_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save()
            return redirect('create_answer', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'main/admin/create_question.html', {'form': form})


@teacher_required
def create_answer(request, pk):
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question # Assigning the question to the answer
            answer.save()
            return redirect('create_answer', pk=question.pk) # Redirect to the same page for adding more answers
    else:
        form = AnswerForm()
    return render(request, 'main/admin/create_answer.html', {'form': form, 'question': question})

@teacher_required
def homesss(request):
    return render(request, 'main/admin/homesss.html')

@student_required
def disciplin_detail_view(request, disciplin_id):
    disciplin = get_object_or_404(Disciplin, id=disciplin_id)
    topics = disciplin.topics.all()
    return render(request, 'main/users/disciplin_detail.html', {'disciplin': disciplin, 'topics': topics})



from django.http import FileResponse
import os
from django.conf import settings

def download_file(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    file_path = os.path.join(settings.MEDIA_ROOT, topic.file.name)

    if os.path.exists(file_path):
        topic.file_downloaded = True
        topic.save(update_fields=['file_downloaded'])
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=topic.file.name)



@teacher_required
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)  # Добавьте request.FILES
        if form.is_valid():
            form.save()
            return redirect('homesss')
    else:
        form = TopicForm()
    return render(request, 'main/admin/create_topic.html', {'form': form})

@student_required
def test_view(request):
    return render(request, 'main/users/test.html')



def chat(request):
    return render(request, 'main/chat.html'
    )

@csrf_exempt
def Ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest': # Check if request is Ajax

        text = request.POST.get('text')
        print(text)

        openai.api_key = "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" # Here you have to add your api key.
        res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{text}"}
        ]
        )

        response = res.choices[0].message["content"]
        print(response)


        return JsonResponse({'data': response,})
    return JsonResponse({})



from django.shortcuts import render, redirect, get_object_or_404
from .forms import FinalQuizForm
from .models import Disciplin, Question, FinalQuizsResult
import random


import random

import random

def final_quiz_view(request, disciplin_id):
    disciplin = get_object_or_404(Disciplin, id=disciplin_id)
    user = request.user

    # Обновление exam_attempts пользователя на основе количества завершенных финальных тестов
    user.exam_attempts = FinalQuizsResult.objects.filter(user=user, disciplin=disciplin, is_completed=True).count()
    user.save()

    # Проверка, не превышено ли максимальное количество попыток
    if user.exam_attempts >= 2:
        return redirect('disciplin')  # Перенаправление на страницу с сообщением о достижении лимита попыток

    # Проверяем, существует ли последний результат теста и не завершен ли он
    final_quiz_result = FinalQuizsResult.objects.filter(user=user, disciplin=disciplin).last()
    if final_quiz_result and not final_quiz_result.is_completed:
        time_passed = timezone.now() - final_quiz_result.start_time
        if time_passed.total_seconds() > 10:  # Проверка на истечение времени
            final_quiz_result.is_completed = True
            final_quiz_result.save()
            # Здесь можно добавить логику для перенаправления на страницу с уведомлением об истечении времени
            return redirect('disciplin')

    if request.method == 'GET':
        # Если теста нет или он завершен, создаем новый экземпляр теста
        if final_quiz_result is None or final_quiz_result.is_completed:
            final_quiz_result = FinalQuizsResult.objects.create(user=user, disciplin=disciplin, start_time=timezone.now())
            user.exam_attempts -= 1

    # Выбираем вопросы из разных блоков
    questions = []
    for block in ['L1', 'L2', 'M1', 'M2', 'H1', 'H2']:
        block_questions = Question.objects.filter(difficulty_block=block, disciplin=disciplin)
        questions.extend(random.sample(list(block_questions), min(5, block_questions.count())))

    if request.method == 'POST':
        final_quiz_result = FinalQuizsResult.objects.get(user=user, disciplin=disciplin, start_time__isnull=False)
        time_passed = timezone.now() - final_quiz_result.start_time

        if time_passed.total_seconds() > 10:  # 7200 секунд = 2 часа
            # Обработка истечения времени
            return redirect('disciplin')  # Перенаправление на страницу с сообщением об истечении времени

        form = FinalQuizForm(request.POST, questions=questions)
        if form.is_valid():
            correct_answers_count = 0
            incorrect_answers = []

            # ...
            for question in questions:
                field_name = f'question_{question.id}'
                user_answer_ids = form.cleaned_data.get(field_name)

                if question.question_type == 'MC':
                    correct_answers = {str(answer.id) for answer in question.answers.filter(is_correct=True)}
                    user_answers_set = set(user_answer_ids)

                    # Получаем тексты ответов по их ID
                    user_answers_texts = [answer.text for answer in question.answers.filter(id__in=user_answer_ids)]

                    if correct_answers == user_answers_set:
                        correct_answers_count += 1
                    else:
                        incorrect_answers.append({'question_id': question.id, 'user_answers': user_answers_texts})
                elif question.question_type == 'TF':
                    correct_answer = question.answers.filter(is_correct=True).first()
                    user_answer_text = user_answer_ids  # В этом случае user_answer_ids уже содержит текст ответа

                    if correct_answer and correct_answer.text.strip().lower() == user_answer_text.strip().lower():
                        correct_answers_count += 1
                    else:
                        incorrect_answers.append({'question_id': question.id, 'user_answer': user_answer_text})

            # Рассчитываем процент правильных ответов и оценку
            percentage = (correct_answers_count / len(questions)) * 100
            grade = 5 if percentage >= 90 else 4 if percentage >= 80 else 3 if percentage >= 70 else 2

            # Сохраняем результат
            FinalQuizsResult.objects.create(
                user=user,
                disciplin=disciplin,
                correct_answers_count=correct_answers_count,
                percentage=percentage,
                grade=grade,
                incorrect_answers=incorrect_answers
            )
            final_quiz_result.is_completed = True
            final_quiz_result.save()

            return redirect('disciplin')  # Перенаправляем на страницу с результатами
    else:
        form = FinalQuizForm(questions=questions)

    return render(request, 'main/users/final_quiz.html', {'form': form, 'disciplin_id': disciplin_id, 'start_time': final_quiz_result.start_time })





@student_required
def incorrect_answers_view(request, quiz_result_id):
    quiz_result = get_object_or_404(QuizResult, id=quiz_result_id)
    incorrect_answers_data = quiz_result.incorrect_answers

    incorrect_questions_with_answers = [
        {
            'question': Question.objects.get(id=answer_data['question_id']),
            'user_answer': answer_data['user_answer'],
            'correct_answer': ', '.join([ans.text for ans in Question.objects.get(id=answer_data['question_id']).answers.filter(is_correct=True)])
        }
        for answer_data in incorrect_answers_data
    ]

    return render(request, 'main/users/incorrect_answers.html', {'incorrect_questions_with_answers': incorrect_questions_with_answers})



def incorrect_final_quiz_view(request, final_quiz_result_id):
    final_quiz_result = get_object_or_404(FinalQuizsResult, id=final_quiz_result_id)
    incorrect_answers_data = final_quiz_result.incorrect_answers

    incorrect_questions_with_answers = []
    for answer_data in incorrect_answers_data:
        question = Question.objects.get(id=answer_data['question_id'])
        correct_answers = ', '.join([ans.text for ans in question.answers.filter(is_correct=True)])

        # Получение ответов пользователя
        user_answers = answer_data.get('user_answers') or answer_data.get('user_answer')

        incorrect_questions_with_answers.append({
            'question': question,
            'user_answers': user_answers,  # передаем как есть, без изменений
            'correct_answer': correct_answers
        })

    return render(request, 'main/users/incorrect_final_quiz_answers.html', {'incorrect_questions_with_answers': incorrect_questions_with_answers})



def view_teacher_results(request):
    if request.user.is_authenticated and request.user.position == 'Преподаватель':
        teacher_disciplines = Disciplin.objects.filter(user=request.user)
        results = []
        for disciplin in teacher_disciplines:
            results.extend(FinalQuizsResult.objects.filter(disciplin=disciplin))
        return render(request, 'main/admin/results.html', {'results': results})
