from oxiterp.settings.base import *

# Override base.py settings here


DEBUG = True
ALLOWED_HOSTS = ['*']

#DATABASES = {
 #   'default': {
  #      'ENGINE': 'django.db.backends.postgresql',
   #     'NAME': 'oxiterp',
    #    'USER': 'oxitowner',
     #   'PASSWORD': 'oxit2016',
      #  'HOST': 'localhost',
       # 'PORT': '5432',
    #}
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'etutproje2',
        'HOST': 'localhost',
        'PORT': '3307',
        'USER': 'root',
        'PASSWORD': 'kobil2013'
    }
}


STATIC_ROOT = "C:/Bitnami/djangostack-2.2.12-0/apache2/htdocs/static2/"

STAICFILES_DIR = [

    "C:/Bitnami/djangostack-2.2.12-0/apache2/htdocs/static2/"

]


try:
    from oxiterp.settings.local import *
except :
    pass
