from django.db import models
from sbs.models.GTapu import GTapu
from sbs.models.EnumFields import EnumFields
from sbs.models.Gkurum import Gkurum


class Gtahsis(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)

    tapu = models.ForeignKey(GTapu, on_delete=models.SET_NULL, verbose_name='Tahsisli Arsa Tapu')
    tahsisTarihi = models.DateTimeField(null=True, blank=True)
    tahsisSuresi = models.CharField(max_length=128, verbose_name='Tahsis Süresi')
    tahsis_amaci = models.CharField(max_length=128, verbose_name='Proje Cinsi', choices=EnumFields.TAHSİS_AMACİ, )
    tahsis_kurum = models.ForeignKey(Gkurum, on_delete=models.SET_NULL, verbose_name='Tahsis Eden Kurum')
    emsal = models.CharField(max_length=128, verbose_name='Tahsis Süresi')
