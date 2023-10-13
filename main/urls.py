from django.urls import path
from .views import (LogoutUserView, BaseView, SignInView, SignUpView, subsection_list, subsection_detail)
from . import views

urlpatterns = [
    path('', BaseView.as_view(), name='base'),#Главная
    path('signup/', SignUpView.as_view(), name='signup'),#Регистрация
    path('signin/', SignInView.as_view(), name='signin'),#Авторизация
    path('logout/', LogoutUserView.as_view(), name='logout'),#Выход
    path('section/<int:section_id>/', subsection_list, name='subsection_list'),
    path('subsection/<int:subsection_id>/', subsection_detail, name='subsection_detail'),
    path('quiz/<int:disciplin_id>/', views.quiz_view, name='quiz'),
    path('create_group/', views.create_group, name='create_group'),
    path('create_discipline/', views.create_discipline, name='create_discipline'),
    path('homesss/', views.homesss, name='homesss'),
    path('create_question/', views.create_question, name='create_question'),
    path('create_answer/<int:pk>/', views.create_answer, name='create_answer'),
    path('disciplin/<int:disciplin_id>/', views.disciplin_detail_view, name='disciplin_detail'),

    # ... другие пути ...
]
