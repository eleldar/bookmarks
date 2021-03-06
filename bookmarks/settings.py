from pathlib import Path
import local_settings
import os
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = local_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

'''Django проверяет домены, перечисленные в настройке ALLOWED_HOSTS.
Это мера предосторожности для предотвращения атак подмены HTTP-заголовков.
Django разрешает использовать только те домены, которые указаны в ALLOWED_HOSTS'''
# явно задали localhost и 127.0.0.1, чтобы иметь возможность обращаться к сайту
# через localhost, который используется Django по умолчанию при настройке DEBUG,
# равной True, и пустом списке ALLOWED_HOSTS
ALLOWED_HOSTS = ['post-o-gram.ru',
                 'localhost',
                 '127.0.0.1',
                 'c4b4a5bba490.ngrok.io']


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
    'images.apps.ImagesConfig',   # приложение для возможности сохранять в закладки картинки, найденные на других сайтах,
                                  # и делиться ими на нашем сайте

    # приложение, которое дает возможность пользователям использовать аккаунты сторонних соцсетей для входа на сайт
    'social_django',

    # приложение, которое позволяет показывать картинки, приведенные к единому размеру, – генерировать их превью
    'sorl.thumbnail',

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
    'django.contrib.messages',     # встроена система сообщений, которая позволяет отображать одноразовые уведомления;
                                   # cистема сообщений предоставляет простой механизм отправлять уведомления пользователям
                                   # (по умолчанию они хранятся в cookie и отображаются при последующем запросе пользователя);
                                   # система сообщений добавляется по умолчанию, если проект был создан с помощью команды python manage.py startproject
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
    'django.contrib.messages.middleware.MessageMiddleware',    # промежуточный слой для системы сообщений, которая позволяет отображать одноразовые уведомления
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookmarks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [ # контекстные процессоры, которые передают сведения в HTML
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages', # добавляет переменную message;
                                                                       # может быть использована в шаблонах для отображения всех существующих уведомлений
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

# Несколько методов аутенификации пользователя.
'''Django будет использовать бэкэнды по порядку, поэтому теперь пользователь сможет аутентифицироваться и с помощью электронной почты.
Идентификационные данные сначала будут проверены ModelBackend. Если этот бэкэнд не вернет объект пользователя, Django попробует аутентифицировать его
с помощью собственного класса, EmailAuthBackend.
Порядок, в котором бэкэнды указаны в настройке AUTHENTICATION_BACKENDS, имеет значение!
Если одни и те же идентификационные данные окажутся корректными для нескольких бэкэндов, Django остановит проверку, как только первый из них вернет объект
пользователя.'''
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # основной бэкэнд ModelBackend, который использует логин и пароль пользователя в качестве идентификационных данных
    'account.authentication.EmailAuthBackend',   # cобственный бэкэнд, который проверяет e-mail вместо логина
    'social_core.backends.facebook.FacebookOAuth2', # facebook
    'social_core.backends.twitter.TwitterOAuth',    # twitter; нет одобрения на сайте Twitter
    'social_core.backends.google.GoogleOAuth2',     # google
]

SOCIAL_AUTH_FACEBOOK_KEY = local_settings.SOCIAL_AUTH_FACEBOOK_KEY
SOCIAL_AUTH_FACEBOOK_SECRET = local_settings.SOCIAL_AUTH_FACEBOOK_SECRET
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email'] # укажем данные, которые хотим запрашивать из Facebook-аккаунта

SOCIAL_AUTH_TWITTER_KEY = local_settings.SOCIAL_AUTH_TWITTER_KEY
SOCIAL_AUTH_TWITTER_SECRET = local_settings.SOCIAL_AUTH_TWITTER_SECRET

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = local_settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = local_settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET


# Django динамически добавляет метод get_absolute_url() для каждой модели,
# перечисленной в настройке ABSOLUTE_URL_OVERRIDES.
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy( # возвращаем URL по имени user_detail
        'user_detail',
        args=[u.username])
}

# При проблемах с формированием превью картинок
# THUMBNAIL_DEBUG = True
