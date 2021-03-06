# Generated by Django 2.2.4 on 2020-05-08 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EPProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True, verbose_name='Branş Adı')),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('operationDate', models.DateTimeField(auto_now=True)),
                ('mimar', models.CharField(blank=True, max_length=120, null=True, verbose_name='Mimar')),
                ('insaatMuhStatik', models.CharField(blank=True, max_length=120, null=True, verbose_name='İnşaat Mühendisi(Statik)')),
                ('makineMuh', models.CharField(blank=True, max_length=120, null=True, verbose_name='Makine Mühendisi')),
                ('elektrikMuh', models.CharField(blank=True, max_length=120, null=True, verbose_name='Elektrik Mühendisi')),
                ('insaatMuhYaklasik', models.CharField(blank=True, max_length=120, null=True, verbose_name='İnşaat Mühendisi(Yaklaşık)')),
                ('elektronikMuh', models.CharField(blank=True, max_length=120, null=True, verbose_name='Elektronik Mühensisi')),
                ('jeofizikMuh', models.CharField(blank=True, max_length=120, null=True, verbose_name='Jeofizik Mühendisi')),
                ('cevreMuh', models.CharField(blank=True, max_length=120, null=True, verbose_name='Çevre Mühendisi')),
                ('peyzajMimari', models.CharField(blank=True, max_length=120, null=True, verbose_name='Peyzaj Mimarı')),
                ('musahitMuh', models.CharField(blank=True, max_length=120, null=True, verbose_name='Müşahit Mühendis')),
                ('butceCinsi', models.CharField(choices=[('Genel/İş Yurtları', 'Genel/İş Yurtları')], default='Genel/İş Yurtları', max_length=128, verbose_name='Bütçe Cinsi')),
                ('butceYili', models.IntegerField(blank=True, null=True)),
                ('projeCinsi', models.CharField(blank=True, max_length=120, null=True, verbose_name='Yapıya Esas Proje Cinsi')),
                ('arsaAlani', models.FloatField(default=0)),
                ('insaatAlani', models.FloatField(default=0)),
                ('tahminiOdenekTutari', models.DecimalField(decimal_places=2, max_digits=12)),
                ('yaklasikMaliyet', models.DecimalField(decimal_places=2, max_digits=12)),
                ('ihaleTarihi', models.DateTimeField()),
                ('sozlesmeBedeli', models.DecimalField(decimal_places=2, max_digits=12)),
                ('sozlesmeTarihi', models.DateTimeField()),
                ('isSUresi', models.IntegerField(default=0)),
                ('isBitimTarihi', models.DateTimeField()),
            ],
            options={
                'default_permissions': (),
            },
        ),
    ]
