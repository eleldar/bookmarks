from django import forms

class LoginForm(forms.Form):
    '''Форма авторизации пользователя'''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) # виджет PasswordInput будет сформирован
                                                           # в HTML как элемент <input> с атрибутом
                                                           # type="password", поэтому браузер будет
                                                           # работать с ним как с полем пароля.