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


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Question, Answer, User

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuizForm, self).__init__(*args, **kwargs)
        for index, question in enumerate(questions, start=1):
            self.fields[f'question_{index}'] = forms.ModelChoiceField(
                queryset=question.answers.all(),
                widget=forms.RadioSelect,
                empty_label=None,
                label=question.text,
            )


@login_required
def quiz_view(request):
    if request.user.difficulty_block:
        questions = Question.objects.filter(difficulty_block=request.user.difficulty_block)
    else:
        questions = Question.objects.filter(difficulty_block__isnull=True)

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            correct_answers_count = sum(1 for q, a in form.cleaned_data.items() if a.is_correct)
            percentage = (correct_answers_count / questions.count()) * 100

            current_block = request.user.difficulty_block
            new_block = ''

            # Блок сложности L1
            if current_block == 'L1':
                new_block = 'L2' if percentage >= 70 else 'L1'

            # Блок сложности L2
            elif current_block == 'L2':
                new_block = 'M1' if percentage > 80 else 'L2' if percentage >= 70 else 'L1'

            # Блок сложности M1
            elif current_block == 'M1':
                new_block = 'M2' if percentage > 80 else 'M1' if percentage >= 70 else 'L2'

            # Блок сложности M2
            elif current_block == 'M2':
                new_block = 'H1' if percentage > 80 else 'M2' if percentage >= 70 else 'M1'

            # Блок сложности H1
            elif current_block == 'H1':
                new_block = 'H2' if percentage > 80 else 'H1' if percentage >= 70 else 'M2'

            # Блок сложности H2
            elif current_block == 'H2':
                new_block = 'H2' if percentage > 90 else 'H1'

            # Сохранение нового блока сложности для пользователя
            request.user.difficulty_block = new_block
            request.user.save()

            return redirect('result')
    else:
        form = QuizForm(questions=questions)

    return render(request, 'main/users/quiz.html', {'form': form})


@login_required
def result_view(request):
    return render(request, 'main/users/result.html')
