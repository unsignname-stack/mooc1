import os
import sys
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'lm=(jf88%up#@qiboy@-rya!0p!y&bun^67iw*8(6uom)cm_nz'

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

SECRET_KEY = '+&&(vzi8w8w6mfqwr5rlwp4#-ywpo$l$7vb1c@ha-sgj&nv47y'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/



# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True
ALLOWED_HOSTS = ['*']
#指定Django后台管理员帐户也使用这个模型类
AUTH_USER_MODEL = 'users.UserProfile'

# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
    # 'djangocomments',
    'django_extensions',
    'corsheaders',  #解决Access-Control-Allow-Origin' header
    'rest_framework',
    'django_filters',
    'users',
    'courses',
    'xadmin',
    'reversion',
    'DjangoUeditor',
    'crispy_forms',
    'rest_framework.authtoken',
    'import_export',
    'QuizAndExam',
    'comments',

]
# from django_extensions.management.commands import graph_models
GRAPH_MODELS = {
  'all_applications': ["users", "courses", "QuizAndExam","comments"],
  'group_models': True,
}
from users.utils import jwt_response_handler
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',#解决Access-Control-Allow-Origin' header
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mooc1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),os.path.join(BASE_DIR, 'static/front')]
        ,
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
CORS_ORIGIN_WHITELIST=(
    #允许跨域白名单
    "http://39.101.79.104",
)
CORS_ALLOW_CREDENTIALS=True #允许白名单的host跨域时携带cookie

WSGI_APPLICATION = 'mooc1.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "aimooc",
        'USER': 'root',
        'PASSWORD': 'root123',
        'HOST': "localhost",
        'PORT':3307,
        "OPTIONS":{"init_command":"SET default_storage_engine=INNODB;"}
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/' #凡是以此开头的url,django 会自动搜索所有app下的static文件夹
STATICFILES_DIRS = [  #='/home/sst/mooc1/static'
    # os.path.join(BASE_DIR, 'static'),
    # os.path.join(BASE_DIR, 'extra_apps/xadmin', 'static')
]
# STATICFILES_DIRS告诉django,首先到STATICFILES_DIRS里面寻找静态文件,其次再到各个app的static文件夹里面找。
# 注意, django查找静态文件是惰性查找,查找到第一个,就停止查找了

STATIC_ROOT = os.path.join(BASE_DIR, 'static/') #文件上传地址(当debug改为true时需要更改)

# 部署django项目的时候需要用到STATIC_ROOT ，它是收集所有的静态文件并放在一个目录里，即STATIC_ROOT指向的目录里。
# 执行完python manage.py collectstatic后，将静态文件复制到STATIC_ROOT指定的目录中。

MEDIA_URL = "/media/" #用于响应请求时提供的资源地址，如 ip:port +MEDIA_URL（/media/） + 数据库保存的资源地址（courses/images/_20220906123433.png）
MEDIA_ROOT = os.path.join(BASE_DIR, "media") #='/home/sst/mooc1/media' 用于上传文件时的基地址

#手机号码正则表达式
REGEX_MOBILE = "^1[3578]\d{9}$|^147\d{8}$|^176\d{8}$"
#云片网设置
APIKEY = "c4a88b7b18bbbf654e9f4f79c9fcb62f"

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 8,
    'DEFAULT_FILTER_BACKENDS':['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',

}
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_RESPONSE_PAYLOAD_HANDLER':jwt_response_handler,
}

AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)

