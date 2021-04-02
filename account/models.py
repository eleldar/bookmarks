from django.db import models
from django.conf import settings

class Profile(models.Model):
    '''собственная модель профиля пользователя'''
    # Чтобы наш код не зависел от конкретной модели пользователя, мы используем функцию get_user_model().
    # Она возвращает модель, указанную в настройке AUTH_USER_MODEL, и мы можем легко заменять класс пользователя,
    # т. к. не обращались в коде напрямую к конкретной модели.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Поле «один к одному» user позволит нам связать дополнительные данные
                                                                                    # с конкретным пользователем. Мы передаем CASCADE в качестве параметра
                                                                                    # on_delete, поэтому связанные с пользователем данные будут удалены при удалении
                                                                                    # основного объекта User.
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True) # Поле photo имеет тип ImageField. Для работы с ним нам необходимо установить библиотеку
                                                                      # изображений Pillow с помощью команды: pip install Pillow==5.1.0
                                                                      # Для того чтобы Django знал, где хранить медиафайлы, загруженные пользователями,
                                                                      # добавим следующие строки в settings.py:
                                                                      # MEDIA_URL = '/media/'
                                                                      # MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

    def __str__(self):
        return f'Профиль для пользователя {self.user.username}'

# Create your models here.
