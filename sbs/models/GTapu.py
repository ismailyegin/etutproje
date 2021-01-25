from django.db import models
from sbs.models.Town import Town
from sbs.models.City import City
from sbs.models.Country import Country


class GTapu(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)

    year = models.DateTimeField(null=True, blank=True)
    area = models.CharField(max_length=120, null=True, blank=True)
    parcel = models.CharField(max_length=120, null=True)
    island = models.CharField(max_length=120, null=True)
    neighborhood = models.TextField(blank=True, null=True, verbose_name='Mahallle')
    location = models.TextField(blank=True, null=True, verbose_name='konum')
    town = models.ForeignKey(Town, on_delete=models.SET_NULL, verbose_name='İlce', db_column='town')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, verbose_name='İl', db_column='city')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, verbose_name='Ülke', db_column='country')
