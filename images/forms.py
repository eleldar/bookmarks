from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    '''форма для сохранения объекта картинки'''
    class Meta:
        model = Image
        fields = ('title', 'url', 'description') # поля title, url, description
        widgets = {'url': forms.HiddenInput, }   # добавим JavaScript-инструмент для выбора картинки на любом постороннем сайте, а наша форма будет получать URL изображения в качестве параметра.
                                                 # Мы заменили виджет по умолчанию для поля url и используем HiddenInput. Этот виджет формируется как input-элемент с атрибутом type="hidden". 
                                                 # Мы сделали это для того, чтобы пользователи не видели поле url.
    def clean_url(self):
        '''валидация полей формы
        Django дает возможность проверять каждое поле формы по отдельности с помощью мето-
        дов вида clean_<fieldname>(). Эти методы вызываются, когда мы обращаемся
        к методу is_valid() формы. Внутри функции валидации мы можем подменять
        значение или генерировать ошибки для конкретного поля.
        '''
        url = self.cleaned_data['url'] # получает значение поля url, обращаясь к атрибуту формы cleaned_data
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower() # разделяет URL, чтобы получить расширение файла и проверить, является ли оно корректным
        if extension not in valid_extensions: # Если это не так, то
            raise forms.ValidationError('Этот URL-адрес не содержит допустимых изображений') # форма генерирует исключение ValidationError
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm, self).save(commit=False) # создает объект image, вызвав метод save() с аргументом commit=False
        image_url = self.cleaned_data['url'] # получаем URL из атрибута cleaned_data формы
        image_name = f'{slugify(image.title)}.{image_url.rsplit(".", 1)[1].lower()}' # генерируем название изображения, совмещая слаг и расширение картинки
        response = request.urlopen(image_url) # используем Python-пакет urllib, чтобы скачать файл картинки
        image.image.save(image_name, ContentFile(response.read()), save=False) # вызываем метод save() поля изображения, передавая в него объект скачанного файла, ContentFile
                                                                               # используется аргумент commit=False, чтобы пока не сохранять объект в базу данных
        # при переопределении метода важно оставить стандартное поведение, поэтому сохраняем объект изображения в базу данных только в том случае, если commit равен True
        if commit:
            image.save()
        return image
