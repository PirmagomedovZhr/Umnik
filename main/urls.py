from django.urls import path
from .views import (LogoutUserView, LadderView, SignInView, SignUpView, DisciplinView)
from . import views

urlpatterns = [

    path('', views.result_view, name='base'),#Главная,
    path('ladder/', LadderView.as_view(), name='ladder'),
    path('signup/', SignUpView.as_view(), name='signup'),#Регистрация
    path('signin/', SignInView.as_view(), name='signin'),#Авторизация
    path('logout/', LogoutUserView.as_view(), name='logout'),#Выход
    path('topics/<int:topic_id>/', views.topic_detail, name='topic_detail'),  # Изменено здесь
    path('quiz/<int:disciplin_id>/', views.quiz_view, name='quiz'),
    path('create_group/', views.create_group, name='create_group'),
    path('create_discipline/', views.create_discipline, name='create_discipline'),
    path('homesss/', views.homesss, name='homesss'),
    path('create_question/', views.create_question, name='create_question'),
    path('create_answer/<int:pk>/', views.create_answer, name='create_answer'),
    path('disciplin/<int:disciplin_id>/', views.disciplin_detail_view, name='disciplin_detail'),
    path('create_topic/', views.create_topic, name='create_topic'),
    path('test/', views.test_view, name='test'),
    path('disciplins/', DisciplinView.as_view(), name='disciplin'),
path('disciplin/<int:disciplin_id>/ladder/', views.LadderView.as_view(), name='ladder'),
    path('chat/', views.chat, name='chat'),
    path('ajax/', views.Ajax, name='ajax'),
    path('discipline_results/<int:disciplin_id>/', views.discipline_results_view, name='discipline_results'),
    path('final_quiz/<int:disciplin_id>/', views.final_quiz_view, name='final_quiz'),
path('discipline/<int:disciplin_id>/final_quiz_results/', views.final_quiz_results_view, name='final_quiz_results'),
path('incorrect_answers/<int:quiz_result_id>/', views.incorrect_answers_view, name='incorrect_answers'),
path('incorrect_final_quiz/<int:final_quiz_result_id>/', views.incorrect_final_quiz_view, name='incorrect_final_quiz'),
path('results/', views.view_teacher_results, name='view_teacher_results'),
path('download/<int:topic_id>/', views.download_file, name='download_file'),
    # ... другие пути ...
]
