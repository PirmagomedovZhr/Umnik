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
        return render(request, self.template_name, {'disciplin_id': disciplin_id})



class DisciplinView(View):
    template_name = 'main/users/disciplin.html'

    def get(self, request):
        if request.user.is_authenticated:
            form = TokenForm()
            user_disciplines = request.user.disciplines.all()
            return render(request, self.template_name, {'form': form, 'user_disciplines': user_disciplines})
        else:
            return HttpResponseRedirect('/signin')

    def post(self, request):
        form = TokenForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            try:
                discipline = Disciplin.objects.get(token=token)
                request.user.disciplines.add(discipline)
            except Disciplin.DoesNotExist:
                pass  # обработка случая, когда дисциплины с таким токеном не существует
            return redirect('disciplin')


def topic_detail(request, topic_id):  # Переименовано для ясности
    topic = Topic.objects.get(id=topic_id)  # Изменено здесь
    return render(request, 'main/users/topic_detail.html', {'topic': topic})  # Изменено здесь


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect('signin')


def quiz_view(request, disciplin_id):
    disciplin = get_object_or_404(Disciplin, id=disciplin_id)

    # Отбираем вопросы, соответствующие сложности пользователя и выбранной дисциплине
    if request.user.difficulty_block:
        questions = Question.objects.filter(difficulty_block=request.user.difficulty_block, disciplin=disciplin)
    else:
        questions = Question.objects.filter(difficulty_block__isnull=True, disciplin=disciplin)


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

            quiz_result = QuizResult(
                user=request.user,
                disciplin=disciplin,
                correct_answers_count=correct_answers_count,
                percentage=percentage
            )
            quiz_result.save()

            return redirect('disciplin')

    else:
        form = QuizForm(questions=questions)


    questions_and_forms = zip(questions, form)
    return render(request, 'main/users/quiz.html',
                  {'questions_and_forms': questions_and_forms, 'disciplin_id': disciplin_id})



from .models import QuizResult

def discipline_results_view(request, disciplin_id):
    disciplin = Disciplin.objects.get(id=disciplin_id)
    results = QuizResult.objects.filter(user=request.user, disciplin=disciplin)

    return render(request, 'main/users/discipline_results.html', {'disciplin': disciplin, 'results': results})



def result_view(request):
    return render(request, 'main/users/base.html')



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




def create_discipline(request):
    if request.method == 'POST':
        form = DisciplineForm(request.POST, user=request.user)  # Добавьте user сюда
        if form.is_valid():
            discipline = form.save(commit=False)
            discipline.user = request.user
            discipline.save()
            return redirect('homesss')
    else:
        form = DisciplineForm(user=request.user)
    return render(request, 'main/admin/create_discipline.html', {'form': form})




def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save()
            return redirect('create_answer', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'main/admin/create_question.html', {'form': form})



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


def homesss(request):
    return render(request, 'main/admin/homesss.html')


def disciplin_detail_view(request, disciplin_id):
    disciplin = get_object_or_404(Disciplin, id=disciplin_id)
    topics = disciplin.topics.all()
    return render(request, 'main/users/disciplin_detail.html', {'disciplin': disciplin, 'topics': topics})



def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save()
            return redirect('homesss')
    else:
        form = TopicForm()
    return render(request, 'main/admin/create_topic.html', {'form': form})


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