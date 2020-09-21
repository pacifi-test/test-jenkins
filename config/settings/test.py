from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": 'almacen_db',
        "USER": 'postgres',
        "PASSWORD": '123456',
        "HOST": 'localhost',
        "PORT": '5432'
    }
}
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
