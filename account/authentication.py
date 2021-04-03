from django.contrib.auth.models import User
'''Django предоставляет способ создания собственного бэкэнда аутентификации. 
Достаточно описать класс, в котором есть два метода:
1. authenticate() – принимает в качестве параметров объект запроса request
и идентификационные данные пользователя. Он должен возвращать
объект пользователя, если данные корректны; в противном случае – None.
Аргумент request имеет тип HttpRequest, но может быть и None;
2. get_user()– принимает ID и должен вернуть соответствующий объект
пользователя.'''

class EmailAuthBackend(object):
    '''Аутентификация пользователя по e-mail'''
    def authenticate(self, request, username=None, password=None):
        '''с помощью метода check_password() модели пользователя
           пытается получить пользователя, соответствующего указанным
           электронной почте и паролю;
           этот метод выполняет шифрование пароля и сравнивает результат
           с тем, который хранится в базе данных'''
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        '''получает пользователя по ID, который задается как аргумент user_id.
           Django использует бэкэнд, который аутентифицировал пользователя,
           чтобы получать объект User на протяжении всей сессии'''
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
