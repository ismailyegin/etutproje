from django.db import models
from sbs.models.GkiraBedeli import GkiraBedeli
from sbs.models.EnumFields import EnumFields


class Gkira(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)

    sahibi = models.CharField(max_length=128, verbose_name='Taşınmazın Sahibi', null=True, blank=True)
    onayTarihi = models.DateTimeField(null=True, blank=True)
    sozlesmeTarihi = models.DateTimeField(null=True, blank=True)
    # son tarih sisteme girilmeli kaç gün oldugunu sistem almali
    sozlesmeSonTarihi = models.DateTimeField(null=True, blank=True)
    kiralamaSuresi = models.CharField(max_length=128, verbose_name='Sözlemşme Bitis Tarihi', null=True, blank=True)
    kirabedeli = models.ManyToManyField(GkiraBedeli)
    adres = models.TextField(blank=True, null=True, verbose_name='Tasınmazin Kira Adresi')
    kapalialan = models.IntegerField(null=True, blank=True)
    tahsis_amaci = models.CharField(max_length=128, verbose_name='Kullanim Amaci', choices=EnumFields.TAHSİS_AMACİ, )

    block = models.IntegerField(blank=True, null=True, )
    floor = models.IntegerField(blank=True, null=True, )
    UsageArea = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
