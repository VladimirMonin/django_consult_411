from pathlib import Path
import os
from django.conf.global_settings import LOGOUT_REDIRECT_URL
from django.urls.converters import REGISTERED_CONVERTERS
from dotenv import load_dotenv
from django.urls import reverse_lazy
# Загружаем переменные окружения из файла .env
load_dotenv()

# C:\PY\ПРИМЕРЫ КОДА\django_consult_411\
# BASE_DIR / templates  -
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "core",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "barbershop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.get_main_menu",
            ],
        },
    },
]

WSGI_APPLICATION = "barbershop.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/
# Стаим русский язык: LANGUAGE_CODE = "ru-ru"
LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Это константа для пути к статическим файлам (на сайте!)
STATIC_URL = "static/"
# Это константа для пути к статическим файлам (на сервере)
# STATIC_ROOT = BASE_DIR / 'static'

# Дополнительные директории для поиска статических файлов во время разработки
# Потому что у нас статика лежит в корне проекта в папке static
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URL - это путь на сайте
# Например barbershop.ru/media/...
# Например в модели Review поле photo = models.- это означает что изображение будет доступно по адресу barbershop.ru/media/...
MEDIA_URL = "/media/"

# Лежать будут в папке media на сервере
# ImageField(upload_to="reviews/") - это означает что изображение будет лежать в папке media/reviews/...
MEDIA_ROOT = BASE_DIR / "media"

MISTRAL_MODERATIONS_GRADES = {
    "hate_and_discrimination": 0.1,  # ненависть и дискриминация
    "sexual": 0.1,  # сексуальный
    "violence_and_threats": 0.1,  # насилие и угрозы
    "dangerous_and_criminal_content": 0.1,  # опасный и криминальный контент
    "selfharm": 0.1,  # самоповреждение
    "health": 0.1,  # здоровье
    "financial": 0.1,  # финансовый
    "law": 0.1,  # закон
    "pii": 0.1,  # личная информация
}


TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")



# Маршруты для авторизации
LOGIN_URL = reverse_lazy("login")

# Стандартные переадресации для авторизации, логаута
LOGIN_REDIRECT_URL = reverse_lazy("landing")
LOGOUT_REDIRECT_URL = reverse_lazy("landing")


# Время жизни сессии в секундах (3 дня)
SESSION_COOKIE_AGE = 60 * 60 * 24 * 3 # 60 секунд * 60 минут * 24 часа * 3 день

# Продлевать жизнь сессии при каждом запросе от пользователя
SESSION_SAVE_EVERY_REQUEST = True

# (Опционально) Выходить из системы при закрытии браузера
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True