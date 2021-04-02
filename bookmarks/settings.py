"""
Django settings for bookmarks project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import local_settings
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = local_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # my apps
    'account.apps.AccountConfig', # размещая приложение первым, гарантируем,
                                  # что именно его шаблоны будут использоваться по
                                  # умолчанию вместо шаблонов, объявленных в других приложениях
                                  # Система аутентификации определяет следующие модели:
                                  # 1. User – модель пользователя с основными полями:
                                  # username, password, email, first_name, last_name и is_active;
                                  # 2. Group – модель группы пользователей;
                                  # 3. Permission – разрешение для пользователя или группы пользователей
                                  # на выполнение определенных действий
                                  # обработчики и формы
    # default apps
    'django.contrib.admin',        # включает несколько шаблонов системы аутентификации,
                                   # которые используются для сайта администрирования;
                                   # поскольку приложение account разместили в начале этого списка
                                   # при совпадении путей Django будет использовать наши шаблоны
                                   # вместо тех, которые определены в других приложениях
    'django.contrib.auth',         # Система аутентификации; включен в список установленных приложений
                                   # Система аутентификации определяет следующие модели:

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [  # Промежуточные слои;
                # Промежуточный слой – это класс с методами, которые выполняются
                # при обработке каждого запроса и формировании ответа
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',    # обрабатывает сессию запроса
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # связывает пользователей и запросы с помощью сессий
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookmarks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookmarks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# login/logout settings
LOGIN_REDIRECT_URL = 'dashboard' # указывает адрес, куда Django будет перенаправлять пользователя при успешной авторизации,
                                 # если не указан GET-параметр next
LOGIN_URL = 'login'   # адрес, куда нужно перенаправлять пользователя для входа в систему,
                      # например из обработчиков с декоратором login_required
LOGOUT_URL = 'logout' # адрес, перейдя по которому, пользователь выйдет из своего аккаунта


# во время разработки и тестирования достаточно настроить Django на отправку сообщений в консоль вместо использования SMTP-сервера. 
# Для этих целей Django предоставляет специальный бэкэнд, который необходимо подключить EMAIL_BACKEND;
# определяет класс, который будет использоваться для отправки электронной почты
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_URL = '/media/'                         # MEDIA_URL – это базовый URL, от которого будут формироваться адреса файлов
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/') # MEDIA_ROOT – путь в файловой системе, где эти файлы будут храниться;
                                              # используем BASE_DIR, чтобы наш код был универсальным, т.к. неизвестен путь в явном виде
