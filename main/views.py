from django.http import HttpResponseRedirect
from .forms import SignUpForm, SignInForm
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.views import View
from .models import User
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect


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


class BaseView(View):
    template_superuser = 'main/admin/base.html'
    template_user = 'main/users/base.html'

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return render(request, self.template_superuser)
            else:
                return render(request, self.template_user)
        else:
            return HttpResponseRedirect('/signin')


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect('signin')



# Импортирование необходимых модулей и моделей из приложения
from django.shortcuts import render, get_object_or_404
from .models import Section, Subsection

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Section


@login_required

def subsection_list(request, section_id):
    # Получение списка всех подразделов, связанных с определенным разделом
    subsections = Subsection.objects.filter(section=section_id)
    # Отображение списка подразделов в шаблоне 'main/subsection_list.html' с использованием функции render()
    return render(request, 'main/users/subsection_list.html', {'subsections': subsections})

def subsection_detail(request, subsection_id):
    # Получение подробной информации о конкретном подразделе
    subsection = get_object_or_404(Subsection, id=subsection_id)
    # Отображение информации о подразделе в шаблоне 'main/subsection_detail.html' с использованием функции render()
    return render(request, 'main/users/subsection_detail.html', {'subsection': subsection})


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Test, Question, Answer, UserTestResult


@login_required
def start_test_view(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    first_question = test.questions.first()
    # Можете добавить логику для установки сессии или что-то подобное
    return redirect('question_view', test_id=test.id, question_id=first_question.id)


@login_required
def question_view(request, test_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    next_question_id = Question.objects.filter(test__id=test_id, id__gt=question_id).first()

    if request.method == 'POST':
        # Сохраняем ответы пользователя в сессии
        user_answers = request.session.get('user_answers', [])
        user_answers.append({
            'question_id': question_id,
            'answer_ids': request.POST.getlist('answers')
        })
        request.session['user_answers'] = user_answers

        if next_question_id:
            return redirect('question_view', test_id=test_id, question_id=next_question_id.id)
        else:
            return redirect('result_view', test_id=test_id)

    return render(request, 'main/users/question.html', {'question': question, 'test_id': test_id})


@login_required
def result_view(request, test_id):
    # Получаем ответы пользователя из сессии и очищаем их
    user_answers = request.session.get('user_answers', [])
    request.session['user_answers'] = []

    # Логика подсчета результатов...
    score = calculate_score(user_answers)

    # Сохраняем результаты в базе данных и отображаем их пользователю
    UserTestResult.objects.create(user=request.user, test_id=test_id, score=score)
    return render(request, 'main/users/result.html', {'score': score})


def calculate_score(user_answers):
    score = 0
    for ua in user_answers:
        question = Question.objects.get(pk=ua['question_id'])
        correct_answers = question.answers.filter(is_correct=True).values_list('id', flat=True)

        if set(map(int, ua['answer_ids'])) == set(correct_answers):
            score += 1  # или ваша собственная логика подсчета баллов

    # Преобразуем в проценты или используем свою логику вычисления процентов
    percentage_score = (score / len(user_answers)) * 100
    return percentage_score
