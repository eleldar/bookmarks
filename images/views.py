from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required # собственный декоратор для ajax
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


@ajax_required  # предотвращает прямое обращение к http://127.0.0.1:8000/images/like/
@login_required # не даст неавторизованным пользователям доступ к этому обработчику
@require_POST   # для обеспечения запроса методом POST; в противном случае будет вызвано исключение HttpResponseNotAllowed (статус ответа 405)
def image_like(request):
    """отмечать картинки как понравившиеся и снимать эту отметку"""
    image_id = request.POST.get('id') # ID изображения, для которого выполняется действие
    action = request.POST.get('action') # действие, которое хочет выполнить пользователь (строковое значение like или unlike)
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user) # используем менеджер отношения «многие ко многим» users_like модели Image для добавления пользователя; при повторной передаче дубликат не создается
            else:
                image.users_like.remove(request.user) # используем менеджер отношения «многие ко многим» users_like модели Image для удаления пользователя; при удалении несуществующего ошибки не будет
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ok'}) # объект JsonResponse возвращает HTTP-ответ с типом application/json и преобразует объекты в JSON


@login_required
def image_list(request):
    images = Image.objects.all() # формируем QuerySet для получения всех изображений, сохраненных в закладки
    paginator = Paginator(images, 8) # создаем объект Paginator и получаем постраничный список картинок
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger: # исключение, если переданная страница не является числом
        images = paginator.page(1) # тогда возвращаем первую
    except EmptyPage: # исключение если желаемой страницы не существует
        if request.is_ajax(): # объекта запроса Django есть метод is_ajax(), который проверяет, сделан ли запрос с помощью XMLHttpRequest
            return HttpResponse('') # возвращаем пустую страницу если получили AJAX-запрос с номером страницы, большим, чем их количество
        images = paginator.page(paginator.num_pages)
    context = {'section': 'images', 'images': images}
    if request.is_ajax(): # для AJAX-запросов
        return render(request, 'images/image/list_ajax.html', context=context) # используем list_ajax.html; содержит только HTML для показа картинок
    return render(request, 'images/image/list.html', context=context) # для стандартных запросов используем list.html; наследуется от base.html и показывает полноценную страницу, на которую добавлен список картинок из list_ajax.html
