# Generated by Django 2.2.6 on 2020-05-17 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbs', '0004_epproject_sozlesmebedelikdv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epproject',
            name='karakteristik',
            field=models.CharField(blank=True, choices=[('İNŞAAT', 'İNŞAAT'), ('ETÜT-PROJE', 'ETÜT-PROJE')], default='ETÜT-PROJE', max_length=120, null=True, verbose_name='Karakteristik'),
        ),
    ]