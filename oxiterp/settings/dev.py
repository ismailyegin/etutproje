from oxiterp.settings.base import *

# Override base.py settings here


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'etutprojepostgre',
#         'USER': 'postgres',
#         'PASSWORD': '1',
#         'HOST': 'localhost',
#         'PORT': '5433',
#     }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'etutProje',
        'USER': 'root',
        'PASSWORD': 'kobil2013',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'Kobil',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }

# }
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#  'default': {
#       'ENGINE': 'django.db.backends.sqlite3',
#     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
# }
# }
try:
    from oxiterp.settings.local import *
except :
    pass
