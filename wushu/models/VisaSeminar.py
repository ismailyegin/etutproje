import enum

from django.db import models

from wushu.models.Coach import Coach
from wushu.models.EnumFields import EnumFields


class VisaSeminar(models.Model):
    OPEN = 'Ön Kayıt Açık'
    CLOSED = 'Ön Kayıt Tamamlandı'
    WAITED = 'Beklemede'

    STATUS_CHOICES = (
        (OPEN,'Ön Kayıt Açık'),
        (CLOSED, 'Ön Kayıt Tamamlandı'),
        (WAITED, 'Beklemede')
    )


    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)


    name = models.CharField(blank=False, null=False, max_length=1000)
    startDate = models.DateTimeField()
    finishDate = models.DateTimeField()
    location = models.CharField(blank=False, null=False, max_length=1000)
    branch = models.CharField(max_length=128, verbose_name='Branş', choices=EnumFields.BRANCH.value)
    status = models.CharField(max_length=128, verbose_name='Kayıt Durumu', choices=STATUS_CHOICES, default=WAITED)
    coach=models.ManyToManyField(Coach)


    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions=()
