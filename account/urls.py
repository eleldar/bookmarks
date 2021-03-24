"""bookmarks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')), # шаблоны URL’ов для обработчиков аутентификации содержатся в django.contrib.auth.urls;
                                                   # заменяют нижеперечисленные шаблоны:
    # #path('login/', views.user_login, name='login'),
    ## переход на обработчик входа пользователя в его аккаунт
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    ## переход на обработчик выхода пользователя из-под его учетной записи
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('', views.dashboard, name='dashboard'),
    ## шаблоны для доступа к обработчикам смены пароля
    #path('password_change/',
    #      auth_views.PasswordChangeView.as_view(), # PasswordChangeView будет проверяет форму смены пароля
    #      name='password_change'),
    #path('password_change/done/',
    #      auth_views.PasswordChangeDoneView.as_view(), # PasswordChangeDoneView отображает сообщение о том, что операция выполнена успешно
    #      name='password_change_done'),
    ## обработчики восставновления пароля
    #path('password_reset/',
    #      auth_views.PasswordResetView.as_view(),
    #      name='password_reset'),
    #path('password_reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(),
    #      name='password_reset_done'),
    #path('reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    #path('reset/done/',
    #      auth_views.PasswordResetCompleteView.as_view(),
    #      name='password_reset_complete'),
]
