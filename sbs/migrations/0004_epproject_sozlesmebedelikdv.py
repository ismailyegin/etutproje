# Generated by Django 2.2.6 on 2020-05-16 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbs', '0003_auto_20200516_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='epproject',
            name='sozlesmeBedeliKdv',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
