import enum

from django.db import models

from wushu.models.Athlete import Athlete
from wushu.models.EnumFields import EnumFields


class Competition(models.Model):
    OPEN = 'Ön Kayıt Açık'
    CLOSED = 'Ön Kayıt Tamamlandı'
    WAITED = 'Beklemede'

    STATUS_CHOICES = (
        (OPEN, 'Ön Kayıt Açık'),
        (CLOSED, 'Ön Kayıt Tamamlandı'),
        (WAITED, 'Beklemede')
    )

    TURKEY = 'Türkiye'
    WORLD = 'Dünya'
    OLYMPIAD = 'Olimpiyat'
    EUROPE = 'Avrupa'

    COMPGENERALTYPE = (
        (TURKEY, 'Türkiye'),
        (WORLD, 'Dünya'),
        (OLYMPIAD, 'Olimpiyat'),
        (EUROPE, 'Avrupa')
    )

    INTERUNIVERSITY = 'Üniversiteler Arası'
    INTERSCHOOL = 'Okullar Arası'
    PERSONAL = 'Ferdi'

    COMPTYPE = (
        (INTERUNIVERSITY, 'Üniversiteler Arası'),
        (INTERSCHOOL, 'Okullar Arası'),
        (PERSONAL, 'Ferdi'),
    )

    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    name = models.CharField(blank=False, null=False, max_length=1000)
    startDate = models.DateTimeField()
    finishDate = models.DateTimeField()
    eventDate = models.CharField(max_length=1000, null=True, blank=True)
    eventPlace = models.CharField(max_length=1000, null=True, blank=True)
    compType = models.IntegerField(null=True, blank=True, choices=COMPTYPE)
    compGeneralType = models.IntegerField(null=True, blank=True, choices=COMPGENERALTYPE)
    juryCount = models.IntegerField(null=True, blank=True)
    eskimi = models.BooleanField(default=False)
    isOpen = models.BooleanField(default=False)
    registerStartDate = models.DateTimeField()
    registerFinishDate = models.DateTimeField()

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions = ()
        # db_table = "competition"
