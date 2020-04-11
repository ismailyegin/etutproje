import enum

from django.db import models

from wushu.models.Athlete import Athlete
from wushu.models.EnumFields import EnumFields


class Competition(models.Model):
    OPEN = 'Ön Kayıt Açık'
    CLOSED = 'Ön Kayıt Tamamlandı'
    WAITED = 'Beklemede'

    STATUS_CHOICES = (
        (OPEN,'Ön Kayıt Açık'),
        (CLOSED, 'Ön Kayıt Tamamlandı'),
        (WAITED, 'Beklemede')
    )

    INTERNATIONAL = 'Uluslararası'
    INTERSCHOOL = 'Okullar Arası'
    INTERUNIVERSITY = 'Üniversiteler Arası'
    NATIONAL = 'Ulusal'

    COMPETITION_TYPE = (
        (INTERNATIONAL, 'Uluslararası'),
        (INTERSCHOOL, 'Okullar Arası'),
        (INTERUNIVERSITY, 'Üniversiteler Arası'),
        (NATIONAL, 'Ulusal')
    )

    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    name = models.CharField(blank=False, null=False, max_length=1000)
    startDate = models.DateTimeField()

    finishDate = models.DateTimeField()
    location = models.CharField(blank=False, null=False, max_length=1000)
    branch = models.CharField(max_length=128, verbose_name='Branş', choices=EnumFields.BRANCH.value)
    subBranch = models.CharField(max_length=128, verbose_name='Alt Branş', choices=EnumFields.SUBBRANCH.value)
    status = models.CharField(max_length=128, verbose_name='Kayıt Durumu', choices=STATUS_CHOICES, default=WAITED)
    type =  models.CharField(max_length=128, verbose_name='Türü', choices=COMPETITION_TYPE, default=NATIONAL)

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions=()
