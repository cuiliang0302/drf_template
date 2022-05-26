"""
Django settings for myblog_api project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from DRF.config.log import *
from DRF.config.simpleui import *
import datetime
import os
from pathlib import Path
import environ

env = environ.Env()
# 如果PROJECT_ENV=prod,读取.env.prod文件，否则读取.env.dev文件。
env_name = env.str('PROJECT_ENV', 'dev')
env.read_env('envs/.env.%s' % env_name)
# env.read_env('envs/.env.dev')
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!

# Application definition


INSTALLED_APPS = [
    'simpleui',  # admin UI
    'corsheaders',  # 允许跨域
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'public',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 允许跨域请求
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DRF.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 媒体资源
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'DRF.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
# 登录认证后端配置
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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# 静态文件存放位置
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF认证
REST_FRAMEWORK = {
    # 全局认证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',  # 基本认证
        'rest_framework.authentication.SessionAuthentication',  # session认证
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # POST请求的Token验证
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    # 全局权限
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',  # 默认仅通过认证的用户才能访问
    # )
}

# JWT配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),  # 配置过期时间
}

# 允许指定访问来源
# CORS_ORIGIN_WHITELIST = (
#     'http://127.0.0.1:8080',
#     'http://localhost:8080',
#     'http://ops_vue:8080',
# )
# 允许携带cookie
CORS_ALLOW_CREDENTIALS = True
# 允许所有
CORS_ORIGIN_ALLOW_ALL = True



# 登录认证后端
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.AllowAllUsersModelBackend',  # 创建用户不自动关联数据库的is_active
                           'django.contrib.auth.backends.ModelBackend',  # 指定Django的modelbackend类
                           )
# 开发与生产环境变量
DEBUG = env.bool('DEBUG', False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
SECRET_KEY = env.str('SECRET_KEY')

DATABASES = {
    'default': env.db_url('DATABASE_URL')
}
if env_name == 'dev':  # [开发环境]
    # 静态资源目录
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static")
    ]
else:  # [生产环境]
    # 指定样式收集目录
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    # 设置redis作为django的缓存设置
    CACHES = {
        'default': env.cache(),
    }
    # 设置redis存储django的session信息
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
    # DRF缓存扩展配置
    REST_FRAMEWORK_EXTENSIONS = {
        # 默认缓存时间
        'DEFAULT_CACHE_RESPONSE_TIMEOUT': 3600,
        # 缓存存储
        'DEFAULT_USE_CACHE': 'default'
    }
