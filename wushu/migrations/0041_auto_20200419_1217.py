# Generated by Django 2.2.6 on 2020-04-19 09:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('wushu', '0040_auto_20200419_0137'),
    ]

    operations = [
        migrations.AddField(
            model_name='visaseminar',
            name='forWhichClazz',
            field=models.CharField(default='antrenör', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='visaseminar',
            name='referee',
            field=models.ManyToManyField(to='wushu.Judge'),
        ),
    ]
