from django.db import models

from sbs.models import City


class EPProject(models.Model):
    GENEL_ISYURTLARI = 'Genel/İş Yurtları'

    BUTCE_CINSI = (
        (GENEL_ISYURTLARI, 'Genel/İş Yurtları'),
    )

    name = models.CharField(blank=True, null=True, max_length=120, verbose_name='Branş Adı')
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)

    mimar = models.CharField(max_length=120, null=True, blank=True, verbose_name='Mimar')
    insaatMuhStatik = models.CharField(max_length=120, null=True, blank=True, verbose_name='İnşaat Mühendisi(Statik)')
    makineMuh = models.CharField(max_length=120, null=True, blank=True, verbose_name='Makine Mühendisi')
    elektrikMuh = models.CharField(max_length=120, null=True, blank=True, verbose_name='Elektrik Mühendisi')
    insaatMuhYaklasik = models.CharField(max_length=120, null=True, blank=True,
                                         verbose_name='İnşaat Mühendisi(Yaklaşık)')
    elektronikMuh = models.CharField(max_length=120, null=True, blank=True, verbose_name='Elektronik Mühensisi')
    jeofizikMuh = models.CharField(max_length=120, null=True, blank=True, verbose_name='Jeofizik Mühendisi')
    cevreMuh = models.CharField(max_length=120, null=True, blank=True, verbose_name='Çevre Mühendisi')
    peyzajMimari = models.CharField(max_length=120, null=True, blank=True, verbose_name='Peyzaj Mimarı')
    musahitMuh = models.CharField(max_length=120, null=True, blank=True, verbose_name='Müşahit Mühendis')
    butceCinsi = models.CharField(max_length=128, verbose_name='Bütçe Cinsi', choices=BUTCE_CINSI,
                                  default=GENEL_ISYURTLARI)

    butceYili = models.IntegerField(blank=True, null=True, )
    projeCinsi = models.CharField(max_length=120, null=True, blank=True, verbose_name='Yapıya Esas Proje Cinsi')
    arsaAlani = models.FloatField(default=0)
    insaatAlani = models.FloatField(default=0)
    tahminiOdenekTutari = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    yaklasikMaliyet = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    ihaleTarihi = models.DateTimeField(null=True,blank=True)
    sozlesmeBedeli = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    sozlesmeTarihi = models.DateTimeField(null=True,blank=True)
    isSUresi = models.IntegerField(default=0)
    isBitimTarihi = models.DateTimeField(null=True,blank=True)

    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl', db_column='city')

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions = ()
