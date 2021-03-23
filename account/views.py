from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm


def user_login(request):
    '''Обработчик авторизации'''
    if request.method == 'POST':
        form = LoginForm(request.POST) # создаем объект формы с данными
        if form.is_valid(): # проверяем, правильно ли заполнена форма;
                            # Если она не валидна, появляется сообщение с ошибками (не заполнение полей)
            cd = form.cleaned_data
            user = authenticate(request, # сверяем данные из формы с данными в базе
                                username=cd['username'],
                                password=cd['password'])
        if user is not None:   # для проверки на корректность введенного логина или пароля
            if user.is_active: # если пользователь был аутентифицирован, проверяем, активен ли он
                login(request, user) # функция login авторизует пользователя на сайте; сохраняет текущего пользователя в сессии
                return HttpResponse('Успешная авторизация')
            else: # если пользователь был аутентифицирован, но не активен!
                return  HttpResponse('Аккаунт не действующий')
        else: # если не корректны введенные логин или пароль
            return HttpResponse('Неверный логин или пароль')
    else: # при вызове методом GET для отображения в шаблоне
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})