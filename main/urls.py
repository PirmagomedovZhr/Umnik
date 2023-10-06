from django.urls import path
from .views import (LogoutUserView, BaseView, SignInView, SignUpView, section_list, subsection_list, subsection_detail)

urlpatterns = [
    path('', BaseView.as_view(), name='base'),#Главная
    path('signup/', SignUpView.as_view(), name='signup'),#Регистрация
    path('signin/', SignInView.as_view(), name='signin'),#Авторизация
    path('logout/', LogoutUserView.as_view(), name='logout'),#Выход
    path('sec/', section_list, name='section_list'),
    path('section/<int:section_id>/', subsection_list, name='subsection_list'),
    path('subsection/<int:subsection_id>/', subsection_detail, name='subsection_detail'),
]
