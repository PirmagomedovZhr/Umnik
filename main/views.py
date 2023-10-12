from django.http import HttpResponseRedirect
from .forms import SignUpForm, SignInForm, QuizForm
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from .models import Section, Subsection, Question
from django.contrib.auth.decorators import login_required



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
                sections = Section.objects.all()
                return render(request, self.template_user, {'sections': sections})
        else:
            return HttpResponseRedirect('/signin')


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect('signin')


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





@login_required
def quiz_view(request):
    if request.user.difficulty_block:
        questions = Question.objects.filter(difficulty_block=request.user.difficulty_block)
    else:
        questions = Question.objects.filter(difficulty_block__isnull=True)

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            correct_answers_count = 0
            for (question, answer_text_or_instance) in zip(questions, form.cleaned_data.values()):
                if question.question_type == 'MC' and answer_text_or_instance.is_correct:
                    correct_answers_count += 1
                elif question.question_type == 'TF':
                    correct_answer = question.answers.filter(is_correct=True).first()
                    if correct_answer and correct_answer.text.strip().lower() == answer_text_or_instance.strip().lower():
                        correct_answers_count += 1

            percentage = (correct_answers_count / questions.count()) * 100
            current_block = request.user.difficulty_block
            new_block = ''

            if current_block == 'L1':
                new_block = 'L2' if percentage >= 70 else 'L1'
            elif current_block == 'L2':
                new_block = 'M1' if percentage > 80 else 'L2' if percentage >= 70 else 'L1'
            elif current_block == 'M1':
                new_block = 'M2' if percentage > 80 else 'M1' if percentage >= 70 else 'L2'
            elif current_block == 'M2':
                new_block = 'H1' if percentage > 80 else 'M2' if percentage >= 70 else 'M1'
            elif current_block == 'H1':
                new_block = 'H2' if percentage > 80 else 'H1' if percentage >= 70 else 'M2'
            elif current_block == 'H2':
                new_block = 'H2' if percentage > 90 else 'H1'

            request.user.difficulty_block = new_block
            request.user.save()

            # Передаем данные для отображения результата в шаблон через session (можно выбрать другой способ)
            request.session['result_data'] = {
                'correct_answers_count': correct_answers_count,
                'percentage': percentage,
                'new_block': new_block
            }

            return redirect('base')

    else:
        form = QuizForm(questions=questions)

    questions_and_forms = zip(questions, form)
    return render(request, 'main/users/quiz.html', {'questions_and_forms': questions_and_forms})


@login_required
def result_view(request):
    return render(request, 'main/users/base.html')
