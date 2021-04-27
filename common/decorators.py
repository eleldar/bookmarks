from django.http import HttpResponseBadRequest

def ajax_required(f):
    """
    декоратор для возрата объекта HttpResponseBadRequest (код ошибки – 400), если запрос не является AJAX-запросом;
    В противном случае возвращается результат выполнения декорируемой функции.
    """
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
