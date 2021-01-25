from django.db import models

from sbs.models.EnumFields import EnumFields
from sbs.models.Gkira import Gkira
from sbs.models.Gtahsis import Gtahsis
from sbs.models.GTapu import GTapu
from sbs.models.Gteskilat import Gteskilat
from sbs.models.Gkurum import Gkurum

Arsa = "Tahsisli Arsa"
Kira = "Kiralık"

TahsisDurumu = (

    (Arsa, 'Tahsisli Arsa '),
    (Kira, 'Kiralık'),
)

Hazine = 'HAZİNE'
Hukumet_konagi_icinde = "HÜKÜMET KONAGI İÇERİSİNDE"
Hukumet_konagi_ayri = "HÜKÜMET KONAGI AYRİ BLOK"
Is_yurtlari = "İŞ YURTLARI"
Diger = "DİĞER KAMU KURUM KURULUŞLARINA AİT YAPILAR"

Mulkiyet = (
    (Hazine, 'HAZİNE'),
    (Hukumet_konagi_icinde, 'HÜKÜMET KONAĞI İÇİNDE'),
    (Hukumet_konagi_ayri, 'HÜKÜMET KONAĞINDA AYRI BLOK'),
    (Is_yurtlari, 'İŞ YURTLARI'),
    (Diger, 'DİĞER KAMU KURUM KURULUŞLARINA AİT YAPILAR'),

)

CIK = 'Ceza İnfaz Kurumu'
AB = 'Adalet Binası'
AT = 'Adli Tıp'
BAM = 'Bölge Adliye Mahkemesi'
BIM = 'Bölge İdare Mahkemesi'
DS = 'Denetimli Serbestlik'
PEM = 'Personel Eğitim Merkezi'
BB = 'Bakanlık Binası'
LOJMAN = 'Lojman'
SOS = "SOSYAL TESİS "
HAK = "HAKİM EVİ"

DIGER = 'Diğer'

TAHSIS_AMACI = (
    (CIK, 'Ceza İnfaz Kurumu'),
    (AB, 'Adalet Binası'),
    (AT, 'Adli Tıp'),
    (BAM, 'Bölge Adliye Mahkemesi'),
    (BIM, 'Bölge İdare Mahkemesi'),
    (DS, 'Denetimli Serbestlik'),
    (BB, 'Bakanlık Bİnası'),
    (PEM, 'Personel Eğitim Merkezi'),
    (LOJMAN, 'Lojman'),

    (SOS, 'Sosyal Tesis'),
    (HAK, 'Hakim Evi'),
    (DIGER, 'Diğer'),
)


class Gtasinmaz(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=120, null=True, blank=True)
    sirano = models.IntegerField(blank=True, null=True, )
    tkgmno = models.IntegerField(blank=True, null=True, )
    tapu = models.ForeignKey(GTapu, on_delete=models.SET_NULL, verbose_name='Tapu', null=True, blank=True)
    kurum = models.ForeignKey(Gkurum, on_delete=models.SET_NULL, verbose_name='Kurum', null=True, blank=True)

    block = models.IntegerField(blank=True, null=True, )
    floor = models.IntegerField(blank=True, null=True)
    UsageArea = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    mulkiyet = models.CharField(max_length=128, verbose_name='Mülkiyet ', choices=Mulkiyet, default=Hazine)

    tahsis_durumu = models.CharField(max_length=128, verbose_name='Tahsis durumu ', choices=TahsisDurumu, default=Arsa)
    tasinmazinTuru = models.CharField(max_length=128, verbose_name='Tasinmazin Türü ', choices=TAHSIS_AMACI, default=AB)

    kira = models.ForeignKey(Gkira, on_delete=models.SET_NULL, verbose_name='Kurum', null=True, blank=True)
    tahsis = models.ForeignKey(Gtahsis, on_delete=models.SET_NULL, verbose_name='Kurum', null=True, blank=True)
    definition = models.CharField(max_length=128, verbose_name='Tasınmaz Açıklama ', null=True, blank=True)
