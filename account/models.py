from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


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

class Contact(models.Model):
    '''Модель для связи с пользователем'''
    user_from = models.ForeignKey('auth.User', # первичный ключ пользователя-подписчика
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', # первичный ключ пользователя-источника
                                 related_name='rel_to_set',
                                 on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, # время создания связи
                                   db_index=True) # индекс по полю created; может ускорить запросы с фильтрацией и сортировкой по нему
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_form} подписан на {self.user_to}'


User.add_to_class('following', # метод add_to_class() динамически добавляет атрибут в модель инфраструктуры Django: User
                  models.ManyToManyField(
                      'self',
                      through=Contact, # добавили промежуточную модель Contact и создали из нее таблицу для связи между пользователями
                      related_name='followers',
                      symmetrical=False) # в явном виде задаем несимметричные отношения, поскольку по умолчанию - симметричные
                 )
