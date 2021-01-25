from django.db import models

from sbs.models.EnumFields import EnumFields
from sbs.models.Gkira import Gkira
from sbs.models.Gdetay import Gdetay
from sbs.models.Gtahsis import Gtahsis
from sbs.models.GTapu import GTapu
from sbs.models.Gteskilat import Gteskilat
from sbs.models.Gkurum import Gkurum


class Gtasinmaz(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=120, null=True)
    sirano = models.IntegerField(blank=True, null=True, )
    tkgmno = models.IntegerField(blank=True, null=True, )
    tapu = models.ForeignKey(GTapu, on_delete=models.SET_NULL, verbose_name='Tapu', null=True, blank=True)
    kurum = models.ForeignKey(Gkurum, on_delete=models.SET_NULL, verbose_name='Kurum', null=True, blank=True)
    block = models.IntegerField(blank=True, null=True, )
    floor = models.IntegerField(blank=True, null=True, )
    UsageArea = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
    mulkiyet = models.CharField(max_length=128, verbose_name='Mülkiyet ', choices=EnumFields.Mulkiyet)

    kira = models.ForeignKey(Gkira, on_delete=models.SET_NULL, verbose_name='Kurum', null=True, blank=True)
    tahsis = models.ForeignKey(Gtahsis, on_delete=models.SET_NULL, verbose_name='Kurum', null=True, blank=True)

    depremDerecesi = models.CharField(max_length=128, verbose_name='Deprem Derecesi', choices=EnumFields.TAHSİS_AMACİ, )

    UsageArea = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
