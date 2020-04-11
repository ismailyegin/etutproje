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
        'NAME': 'oxit-wushu',
        'HOST': 'localhost',
        'PORT': '3307',
        'USER': 'bitnami',
        'PASSWORD': '00babf99dc'
    }
}


STATIC_ROOT = "C:/Bitnami/djangostack-2.2.5-0/apache2/htdocs/static/"

STAICFILES_DIR = [

    "C:/Bitnami/djangostack-2.2.5-0/apache2/htdocs/static/"

]


try:
    from oxiterp.settings.local import *
except :
    pass
