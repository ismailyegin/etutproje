from django.core.validators import RegexValidator, DecimalValidator
from django.db import models

from sbs.models import City
from sbs.models.EPEmployee import EPEmployee
from sbs.models.EPRequirements import EPRequirements
from sbs.models.EPPhase import EPPhase
from sbs.models.EPOffer import EPOffer

class EPProject(models.Model):
    GENEL = 'Genel'
    ISYURTLARI = 'İş Yurtları'

    BUTCE_CINSI = (
        (GENEL, 'Genel'),
        (ISYURTLARI, 'İş Yurtları'),
    )

    CIK = 'Ceza İnfaz Kurumu'
    AB = 'Adalet Binası'
    AT = 'Adli Tıp'
    BAM = 'Bölge Adliye Mahkemesi'
    BIM = 'Bölge İdare Mahkemesi'
    DS = 'Denetimli Serbestlik'
    PEM = 'Personel Eğitim Merkezi'
    BB = 'Bakanlık Bİnası'
    DIGER = 'Diğer'

    PROJE_CINSI = (
        (CIK, 'Ceza İnfaz Kurumu'),
        (AB, 'Adalet Binası'),
        (AT, 'Adli Tıp'),
        (BAM, 'Bölge Adliye Mahkemesi'),
        (BIM, 'Bölge İdare Mahkemesi'),
        (DS, 'Denetimli Serbestlik'),
        (BB, 'Bakanlık Bİnası'),
        (PEM, 'Personel Eğitim Merkezi'),
        (DIGER, 'Diğer'),
    )

    name = models.CharField(blank=True, null=True, max_length=120, verbose_name='Branş Adı')
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)

    employees = models.ManyToManyField(EPEmployee,related_name='personel')
    requirements = models.ManyToManyField(EPRequirements)
    phases = models.ManyToManyField(EPPhase)
    offers = models.ManyToManyField(EPOffer)

    butceCinsi = models.CharField(max_length=128, verbose_name='Bütçe Cinsi', choices=BUTCE_CINSI, )
    butceYili = models.IntegerField(blank=True, null=True, )
    projeCinsi = models.CharField(max_length=128, verbose_name='Bütçe Cinsi', choices=PROJE_CINSI, )
    arsaAlani = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    insaatAlani = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tahminiOdenekTutari = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    yaklasikMaliyet = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    ihaleTarihi = models.DateTimeField(null=True, blank=True)
    sozlesmeBedeli = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sozlesmeTarihi = models.DateTimeField(null=True, blank=True)
    isSUresi = models.IntegerField(null=True, blank=True)
    isBitimTarihi = models.DateTimeField(null=True, blank=True)
    sorumlu=models.ForeignKey(EPEmployee, on_delete=models.CASCADE, verbose_name='Sorumlu',related_name='sorumlu')

    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl', db_column='city')

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions = ()
