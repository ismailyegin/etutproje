from django.db import models

from sbs.models.EnumFields import EnumFields


class Gteskilat(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)

    depremderecesi = models.CharField(max_length=128, verbose_name='deprem derecesi',
                                      choices=EnumFields.DEPREM_DERECE, )
    yargiBolgesi = models.CharField(max_length=128, verbose_name='Yargi Bölgesi', choices=EnumFields.Yargi_bolgesi, )
    merkeznufus = models.IntegerField(blank=True, null=True, )
    yargiAlaniNufus = models.IntegerField(blank=True, null=True, )
    agırCezaMerkezi = models.CharField(max_length=128, blank=True, null=True, )
    asliyeCezaMerkezi = models.CharField(max_length=128, blank=True, null=True, )
    hakim_sayisi = models.CharField(max_length=128, blank=True, null=True, )
    savci_sayisi = models.IntegerField(blank=True, null=True, )
    personel_sayisi = models.IntegerField(blank=True, null=True, )

    UsageArea = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
