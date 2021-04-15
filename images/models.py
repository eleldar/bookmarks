from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Image(models.Model):
    '''Модель для сохранения изображений, добавленных в закладки'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL,      # пользователь, который добавляет изображение в закладки; поле является внешним ключом
                                                           # и использует связь «один ко многим». Пользователь может сохранять много изображений,
                                                           # но каждая картинка может быть сохранена только одним пользователем;
                            related_name='images_created', # имя images_created будет использоваться в отношении "многие ко многим".
                            on_delete=models.CASCADE)
    title = models.CharField(max_length=200)               # заголовок картинки
    slug = models.SlugField(max_length=200, blank=True)    # краткое наименование картинки (слаг); может содержать только буквы, цифры, нижние подчеркивания, дефисы,
                                                           # используется для создания семантических URL’ов
    url = models.URLField() # ссылка на оригинальную картинку
    image = models.ImageField(upload_to='images/%Y/%m/%d') # файл изображения
    description = models.TextField(blank=True)              # необязательное поле описания
    created = models.DateField(auto_now_add=True, db_index = True) # дата и время создания объекта в базе данных;
                                                                   # при auto_now_add текущие время и дата проставляются автоматически;
                                                                   # при db_index=True создается индекс по этому полю
                                                                   # Примечание:
                                                                   # Индексы баз данных улучшают производительность;
                                                                   # для полей с unique=True и ForeignKey индексы создаются автоматически;
                                                                   # для определения составного индекса можно использовать Meta.index_together.
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,    # создает промежуточную таблицу, содержащую первичные ключи объектов связанных моделей.
                                        related_name='images_liked', # Поле ManyToManyField может быть определено в любой из них.
                                        blank=True)                  # ManyToManyField позволяет указать название атрибута, по которому будут доступны связанные объекты.
                                                                     # Этот тип поля предоставляет менеджер отношения «многие ко многим», с помощью которого можно обращаться
                                                                     # к связанным объектам в виде image.users_like.all() или из объекта пользователя user как user.images_likes.all()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        '''автоматически формирует слаг на основе заголовка картинки'''
        if not self.slug:  # при отсутствии слага
            self.slug = slugify(self.title) # функция slugify() автоматически формирует его из переданного заголовка
        super(Image, self).save(*args, **kwargs)
