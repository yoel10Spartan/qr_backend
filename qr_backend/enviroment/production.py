from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_URL = 'static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'qr',
        'USER': 'root',
        'PASSWORD': '3#y^bWJGLAMd',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}