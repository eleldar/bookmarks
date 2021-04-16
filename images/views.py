from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image

@login_required
def image_create(request):
    '''получает начальные данные и создает объект формы.
    Эти данные содержат url и title картинки со стороннего сайта;
    они будут переданы в качестве аргументов GET-запроса JavaScript-инструментом'''
    if request.method == 'POST':
        # Отправлена форма
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # Данные формы валидны
            cd = form.cleaned_data

            new_item = form.save(commit=False) # создает новый объект Image, но пока не сохраняет его в базу данных, передавая аргумент commit=False
            # Добавляем пользователя к созданному объекту
            new_item.user = request.user # привязывает текущего пользователя к картинке
            new_item.save() # сохраняет объект image в базу данных
            messages.success(request, 'Изображение упешно добавлено') # создает уведомление
            # Перенаправляем пользователя на страницу сохраненного изображения
            return redirect(new_item.get_absolute_url()) # перенаправляет пользователя на канонический URL новой картинки
    else:
        # Заполняем форму данными из GET-запроса
        form = ImageCreateForm(data=request.GET)
    context = {'section': 'images', 'form': form}
    return render(request, 'images/image/create.html', context=context)


def image_detail(request, id, slug):
    """Показ сведений об изображении"""
    image = get_object_or_404(Image, id=id, slug=slug)
    context = {'section': 'images', 'image': image}
    return render(request, 'images/image/detail.html', context=context)
