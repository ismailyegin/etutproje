from django.core.validators import RegexValidator, DecimalValidator
from django.db import models

from sbs.models import City
from sbs.models.Town import Town
from sbs.models.EPEmployee import EPEmployee
from sbs.models.Employee import Employee
from sbs.models.EPRequirements import EPRequirements
from sbs.models.EPPhase import EPPhase
from sbs.models.EPOffer import EPOffer
from sbs.models.EPDocument import EPDocument
from sbs.models.EPVest import EPVest
from sbs.models.Company import Company
from sbs.models.SubCompany import SubCompany
from sbs.models.EPNeedDocument import EPNeedDocument
class EPProject(models.Model):



    INSAAT = 'İNŞAAT'
    ETUTPROJE = 'ETÜT-PROJE'

    CHARACTERİSTİC = (
        (INSAAT, 'İNŞAAT'),
        (ETUTPROJE, 'ETÜT-PROJE'),
    )

    PDE = 'Proje devam ediyor'
    PT = 'Proje tamamlandı'
    DYRY = 'Deprem Yön. revizyonu yapılıyor'
    IH='İhale sürecinde'
    PD = 'Proje Durduruldu'
    PIE='Proje İptal Edildi'

    STATUS_CHOICES = (
        (PDE, 'Proje devam ediyor'),
        (PT, 'Proje tamamlandı'),
        (DYRY, 'Deprem Yön. revizyonu yapılıyor'),
        (IH,'İhale sürecinde'),
        (PIE,'Proje İptal Edildi'),
        (PD,'Proje Durduruldu'),
    )



    GENEL = 'Genel'
    ISYURTLARI = 'İş Yurtları'
    BIRIMDISI='Birim Dışı'
    ATGV = 'ATGV  '


    BUTCE_CINSI = (
        (GENEL, 'Genel'),
        (ISYURTLARI, 'İş Yurtları'),
        (BIRIMDISI,'Birim Dışı'),
        (ATGV, 'ATGV '),

    )

    CIK = 'Ceza İnfaz Kurumu'
    AB = 'Adalet Binası'
    AT = 'Adli Tıp'
    BAM = 'Bölge Adliye Mahkemesi'
    BIM = 'Bölge İdare Mahkemesi'
    DS = 'Denetimli Serbestlik'
    PEM = 'Personel Eğitim Merkezi'
    BB = 'Bakanlık Binası'
    LOJMAN='Lojman'

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
        (LOJMAN, 'Lojman'),
        (ATGV, 'ATGV '),
        (DIGER, 'Diğer'),

    )

    name = models.CharField(blank=False, null=False, max_length=120, verbose_name='Branş Adı')
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)

    employees = models.ManyToManyField(EPEmployee,related_name='personel')
    requirements = models.ManyToManyField(EPRequirements)
    phases = models.ManyToManyField(EPPhase)
    offers = models.ManyToManyField(EPOffer)
    vest = models.ManyToManyField(EPVest)

    butceCinsi = models.CharField(max_length=128, verbose_name='Bütçe Cinsi', choices=BUTCE_CINSI, )
    butceYili = models.IntegerField(blank=False, null=False, )
    projeCinsi = models.CharField(max_length=128, verbose_name='Proje Cinsi', choices=PROJE_CINSI, )
    arsaAlani = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,default=0)
    insaatAlani = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,default=0)
    tahminiOdenekTutari = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,default=0)
    yaklasikMaliyet = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,default=0)
    ihaleTarihi = models.DateTimeField(null=True, blank=True)
    sozlesmeBedeli = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,default=0)
    sozlesmeBedeliKdv=models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,default=0)


    sozlesmeTarihi = models.DateTimeField(null=True, blank=True)
    isSUresi = models.IntegerField(null=True, blank=True)
    isBitimTarihi = models.DateTimeField(null=True, blank=True)
    sorumlu=models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Sorumlu',related_name='sorumlu',null=True, blank=True)

    town = models.CharField(blank=True, null=True, max_length=120, verbose_name='ilçe')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl', db_column='city')


    documents=models.ManyToManyField(EPDocument)
    needDocument = models.ManyToManyField(EPNeedDocument)

    # projenin durumu ve  karakteristik  genel bilgiler
    karakteristik=models.CharField(blank=True, null=True, max_length=120, verbose_name='Karakteristik', choices=CHARACTERİSTİC, default=ETUTPROJE)
    projectStatus=models.CharField(max_length=128, verbose_name='Onay Durumu', choices=STATUS_CHOICES)
    # alim isinin=>Ai
    aistart = models.DateTimeField(null=True, blank=True)
    aifinish = models.DateTimeField(null=True, blank=True)
    # ihale eklentileri
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, verbose_name='Sirket', related_name='Sirket',
                                null=True, blank=True)
    subcompany = models.ManyToManyField(SubCompany)



    #
    # ihaleProjeBurosuName = models.CharField(blank=True, null=True, max_length=120, verbose_name='Branş Adı')
    # ihaletel = models.CharField(blank=True, null=True, max_length=120, verbose_name='İletişim (telefon)')
    # ihaleimail = models.CharField(blank=True, null=True, max_length=120, verbose_name='İletişim (mail) ')
    # ihalemuellif = models.CharField(blank=True, null=True, max_length=120, verbose_name='Müellif Adı soyadı')




    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions = ()
