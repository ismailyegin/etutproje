# Generated by Django 2.2.6 on 2020-04-23 22:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('wushu', '0046_auto_20200424_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simlecategory',
            name='area',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='simlecategory',
            name='compCategoryCompleted',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='simlecategory',
            name='compOrder',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='simlecategory',
            name='competition',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='simlecategory',
            name='isDuilian',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='simlecategory',
            name='kobilId',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='simlecategory',
            name='playersOrdered',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='simlecategory',
            name='recordCompleted',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
