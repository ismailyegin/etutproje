# Generated by Django 2.2.6 on 2020-05-14 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbs', '0002_epproject_town'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epproject',
            name='town',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='ilçe'),
        ),
    ]
