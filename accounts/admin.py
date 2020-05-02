from django.contrib import admin
from sbs.models.CategoryItem import CategoryItem
from rest_framework.authtoken.models import Token

# Register your models here.
admin.site.register(CategoryItem)
