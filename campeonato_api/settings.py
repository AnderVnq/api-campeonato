import os
from decouple import Config, Csv,RepositoryIni
from dotenv import load_dotenv
from datetime import timedelta
from firebase_admin import auth,credentials
import firebase_admin
import dj_database_url

load_dotenv()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
firebase_credentials_path = os.environ.get('FIREBASE_CREDENTIALS_PATH')
cred = credentials.Certificate(firebase_credentials_path)

firebase_admin.initialize_app(cred)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEBUG = 'RENDER' not in os.environ


# cred = credentials.Certificate('prueba2-de8dc-firebase-adminsdk-j3vqi-51bb1c980e.json')

# firebase_admin.initialize_app(cred)



ALLOWED_HOSTS = []

# Application definition
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)



BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS=[
    'apps.base',
    'apps.campeonatos',
    'apps.encuentros',
    'apps.equipos',
    'apps.jugadores',
    'apps.users',
    'apps.arbitros',

]


THIRD_APPS=[
    'rest_framework',
    'simple_history',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'corsheaders'
]

INSTALLED_APPS=BASE_APPS+LOCAL_APPS+THIRD_APPS


SWAGGER_SETTINGS={
    'DOC_EXPANSION':'none',
    'SECURITY_DEFINITIONS': {
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      }
   }
}



MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware'
]

ROOT_URLCONF = 'campeonato_api.urls'



REST_FRAMEWORK ={

    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    # Resto de tu configuración
}







TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'apps', 'base', 'templates')],
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

WSGI_APPLICATION = 'campeonato_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE':'mssql', #'django.db.backends.postgresql',
#         'NAME': os.environ.get('NAME_DATABASE'),
#         'USER':os.environ.get('USER_DATABASE'),
#         'PASSWORD':os.environ.get('PASSWORD'),
#         'HOST':os.environ.get('HOST_DATABASE'),
#         'PORT':os.environ.get('PORT_DATABASE',default='5432')
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE':'mssql',
#         'NAME': 'Campeonatos',
#         # 'USER':'apis',
#         # 'PASSWORD':'heaveny2',
#         'HOST': 'ANDER\SQLSERVER',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#             'Trusted_Connection': 'yes',  # Habilita la autenticación de Windows
#         },
#     },
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'Campeonato',
#         'USER': 'root',
#         'PASSWORD': 'heaveny2',
#         'HOST': 'localhost',  # O la dirección IP de tu servidor MySQL
#         'PORT': '3306',       # El puerto predeterminado de MySQL es 3306
#         'OPTIONS': {
#             # Opciones adicionales si es necesario
#         },
#     }
# }
DATABASES = {
   'default': dj_database_url.config(
        default='mysql://root:heaveny2@localhost:3306/Campeonato',
        conn_max_age=600
    )
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


CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:4200',
    # Añade aquí otros dominios o puertos que necesiten acceso a tu API
]

SIMPLE_JWT={
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    'ROTATE_REFRESH_TOKENS':True,
    'BLACKLIST_AFTER_ROTATION':True
}


AUTH_USER_MODEL = 'users.User' 

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



DEFAULT_FROM_EMAIL=os.environ.get("DEFAULT_FROM_EMAIL")
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=DEFAULT_FROM_EMAIL
EMAIL_HOST_PASSWORD=os.environ.get("EMAIL_HOST_PASSWORD")





# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES=(BASE_DIR,'static')
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'      