from django.urls import path
from .views import (LogoutUserView, LadderView, SignInView, SignUpView, DisciplinView)
from . import views

urlpatterns = [

    #path('', BaseView.as_view(), name='base'),#Главная,
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

    # ... другие пути ...
]
