from django.contrib import admin
from .models import Profile

@admin.register(Profile) # регистрация модели Profile на сайте администрирования
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
