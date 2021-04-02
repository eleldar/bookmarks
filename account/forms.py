from django import forms
from django.contrib.auth.models import User
from .models import Profile # для добавления возможности редактировать профиль пользователя через сайт

class LoginForm(forms.Form):
    '''Форма авторизации пользователя'''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) # виджет PasswordInput будет сформирован
                                                           # в HTML как элемент <input> с атрибутом
                                                           # type="password", поэтому браузер будет
                                                           # работать с ним как с полем пароля.

class UserRegistrationForm(forms.ModelForm):
    '''Форма регистрации нового пользователя;
    добавили два поля: password и password2 – для задания и подтверждения пароля'''
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        '''Модельная формя для пользователя; включает поля username, first_name и email.
        Они будут валидироваться в соответствии с типом полей модели.
        В т.ч. если пользователь введет логин, который уже используется,
        ему вернется сообщение с указанием на ошибку, из-за того что
        в модели поле username определено как unique=True'''
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        '''Можно добавлять методы с названием вида clean_<fieldname>() для любого поля формы,
           чтобы Django проверял соответствующее поле и в случае некорректных данных
           привязывал ошибку к нему.
           Кроме того, у форм реализован метод clean(), который проверяет корректность всей формы;
           применяется, когда необходимо выполнить проверку взаимосвязанных полей'''
        cd = self.cleaned_data # проверяем, совпадают ли оба пароля
        if cd['password'] != cd['password2']: # Если они отличаться, то будет возвращена ошибка.
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    '''позволит пользователям менять имя, фамилию, e-mail (поля встроенной в Django модели)'''
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    '''позволит модифицировать дополнительные сведения, которые мы сохраняем в модели Profile (дату рождения и аватар)'''
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
