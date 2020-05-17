# Generated by Django 2.2.6 on 2020-05-17 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sbs', '0005_auto_20200518_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epproject',
            name='butceYili',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='epproject',
            name='name',
            field=models.CharField(default=1, max_length=120, verbose_name='Branş Adı'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='epproject',
            name='sorumlu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sorumlu', to='sbs.Employee', verbose_name='Sorumlu'),
        ),
    ]
