from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages

@login_required
def dashboard(request): # обработчик обернут в декоратор login_required.
                        # Он проверяет, авторизован ли пользователь.
                        # Если пользователь авторизован, Django выполняет обработку.
                        # В противном случае пользователь перенаправляется на страницу логина
                        # При этом в GET-параметре задается next -адрес запрашиваемой страницы.
                        # Таким образом, после успешного прохождения авторизации пользователь
                        # будет перенаправлен на страницу, куда он пытался попасть.
                        # Именно для этих целей передавалось скрытое поле next в форму логина.
    '''Обработчик для отображения рабочего стола,
    который пользователь увидит при входе в свой аккаунт.'''
    context = {'section': 'dashboard'} # добавили переменную контекста section, с помощью которой сможем узнать,
                                       # какой раздел сайта сейчас просматривает пользователь
    return render(request, 'account/dashboard.html', context=context)


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

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя без сохранения в БД
            new_user = user_form.save(commit=False)
            # Создаем пользователю зашифрованный пароль
            new_user.set_password(user_form.cleaned_data['password']) # метод set_password() модели User сохранит пароль в зашифрованном виде
            # Сохраняем пользователя в БД
            new_user.save()
            # Создание профиля пользователя
            Profile.objects.create(user=new_user) # Когда пользователь регистрируется на сайте создается пустой профиль, ассоциированный с ним.
                                                  # Для тех пользователей, которые были созданы ранее, необходимо вручную добавить объекты Profile
                                                  # через сайт администрирования.
            context = {'new_user': new_user}
            return render(request, 'account/register_done.html', context=context)
    else:
        user_form = UserRegistrationForm()
    context = {'user_form': user_form}
    return render(request, 'account/register.html', context=context)

@login_required # обернули функцию в декоратор login_required, потому что для изменения профиля пользователь должен быть авторизован
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST) # форма для базовых сведений о пользователе
        profile_form = ProfileEditForm(instance=request.user.profile,      # форма для дополнительной, расширенной информации
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid(): # для проверки вызываем метод is_valid() каждой из форм
            user_form.save()                                 # Если обе формы заполнены корректно, сохраняем их с помощью метода save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен') # уведомление об успешном изменении данных профиля; используется модуль messages
        else:
            messages.error(request, 'Ошибка обновления профиля') # уведомление об ошибке при изменении данных профиля; используется модуль messages
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'account/edit.html', context=context)
