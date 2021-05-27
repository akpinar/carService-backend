from oxiterp.settings.base import *

# Override base.py settings here


DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'oxit_service',
        'USER': 'oxitowner',
        'PASSWORD': 'oxit2016',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

EMAIL_HOST = "smtp.yandex.com.tr"
EMAIL_HOST_USER = "servis@kulmer.com.tr"
EMAIL_HOST_PASSWORD ="Servis2021"
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False

STATIC_ROOT = "/var/www/static/service"

STAICFILES_DIR = [

    "/var/www/static/service"

]

try:
    from oxiterp.settings.local import *
except:
    pass
