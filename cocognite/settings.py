import environ
import os
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

""" CONFIGURATIONS -----------------------------------------------------------------------------------------------"""

AUTH_USER_MODEL = 'accounts.User'
ROOT_URLCONF = 'cocognite.urls'
WSGI_APPLICATION = 'cocognite.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
SECRET_KEY = env('DJANGO_SECRET_KEY')

DEBUG = True
SERVER = True
SITE_ID = 1

if SERVER:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

    DOMAIN_URL = 'https://rsonlineaccounting.com/'
    GOOGLE_CALLBACK_ADDRESS = "rsonlineaccounting.com/accounts/google/login/callback/"
    STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY_LIVE')
    STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY_LIVE')
else:
    ALLOWED_HOSTS = ['*']
    DOMAIN_URL = 'http://127.0.0.1:8000/'
    GOOGLE_CALLBACK_ADDRESS = "http://127.0.0.1:8000/accounts/google/login/callback/"
    STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY_TEST')
    STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY_TEST')

LOGIN_REDIRECT_URL = '/accounts/cross-auth/'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

""" INSTALLATIONS ------------------------------------------------------------------------------------------------"""

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # REQUIRED_APPLICATIONS
    'crispy_forms',
    'crispy_bootstrap5',
        
    # AUTH_API
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # USER_APPLICATIONS
    'src.accounts',
    'src.website',

    'src.portals.admins',

    # MUST BE AT THE END
]


""" SECURITY AND MIDDLEWARES -------------------------------------------------------------------------------------"""

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

""" TEMPLATES AND DATABASES -------------------------------------------------------------------------------------- """
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


if SERVER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'OPTIONS': {'charset': 'utf8mb4'},
    #         'NAME': env('DATABASE_NAME'),
    #         'USER': env('DATABASE_USER'),
    #         'PASSWORD': env('DATABASE_PASSWORD'),
    #     }
    # }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

""" INTERNATIONALIZATION ----------------------------------------------------------------------------------------- """

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_L10N = True
USE_TZ = True

""" PATHS STATIC AND MEDIA --------------------------------------------------------------------------------------- """

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


if SERVER:
    MEDIA_ROOT = os.path.join(BASE_DIR, '/home/rsonlfwy/public_html/media')
    STATIC_ROOT = os.path.join(BASE_DIR, '/home/rsonlfwy/public_html/assets')
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

""" EMAIL AND ALL AUTH ------------------------------------------------------------------------------------------- """

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

SOCIALACCOUNT_PROVIDERS = {
    'google': {'SCOPE': ['profile', 'email', ],
               'AUTH_PARAMS': {'access_type': 'online', }}
}

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_EMAIL_VERIFICATION = 'none'

""" RESIZER IMAGE --------------------------------------------------------------------------------"""
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {
    'JPEG': ".jpg",
    'PNG': ".png",
    'GIF': ".gif"
}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True
