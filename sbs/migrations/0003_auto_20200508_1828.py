# Generated by Django 2.2.4 on 2020-05-08 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbs', '0002_epproject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epproject',
            name='ihaleTarihi',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='epproject',
            name='isBitimTarihi',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='epproject',
            name='sozlesmeBedeli',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='epproject',
            name='sozlesmeTarihi',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='epproject',
            name='tahminiOdenekTutari',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='epproject',
            name='yaklasikMaliyet',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
