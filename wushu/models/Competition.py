import enum

from django.db import models

from wushu.models.Athlete import Athlete
from wushu.models.EnumFields import EnumFields












class Competition(models.Model):
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

    compType = models.IntegerField(db_column='compType', blank=True, null=True, choices=COMPTYPE)  # Field name made lowercase.
    creationDate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    finishDate = models.DateTimeField(db_column='finishDate', blank=True, null=True)  # Field name made lowercase.
    kobilId = models.IntegerField(db_column='kobilId')  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    operationDate = models.DateTimeField(db_column='operationDate', blank=True, null=True)  # Field name made lowercase.
    startDate = models.DateTimeField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    eventPlace = models.CharField(db_column='eventPlace', max_length=45, blank=True, null=True)  # Field name made lowercase.
    eventDate = models.CharField(db_column='eventDate', max_length=45, blank=True, null=True)  # Field name made lowercase.
    juryCount = models.IntegerField(db_column='juryCount', blank=True, null=True)  # Field name made lowercase.
    compGeneralType = models.IntegerField(db_column='compGeneralType', blank=True, null=True, choices=COMPGENERALTYPE)  # Field name made lowercase.
    eskimi = models.IntegerField(blank=True, null=True)
    isOpen = models.IntegerField(db_column='isOpen', blank=True, null=True)  # Field name made lowercase.
    registerStartDate = models.DateTimeField(db_column='registerStartDate', blank=True, null=True)  # Field name made lowercase.
    registerFinishDate = models.DateTimeField(db_column='registerFinishDate', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        managed = False
        db_table = 'competition'
        default_permissions = ()



