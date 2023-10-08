from django.urls import path
from .views import (LogoutUserView, BaseView, SignInView, SignUpView, subsection_list, )
from . import views
urlpatterns = [
    path('', BaseView.as_view(), name='base'),#Главная
    path('signup/', SignUpView.as_view(), name='signup'),#Регистрация
    path('signin/', SignInView.as_view(), name='signin'),#Авторизация
    path('logout/', LogoutUserView.as_view(), name='logout'),#Выход
    path('section/<int:section_id>/', subsection_list, name='subsection_list'),
    path('start_test/<int:test_id>/', views.start_test_view, name='start_test'),
    path('test/<int:test_id>/question/<int:question_id>/', views.question_view, name='question_view'),
    path('test/<int:test_id>/results/', views.result_view, name='result_view'),

]
