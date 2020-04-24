# Generated by Django 2.2.6 on 2020-04-23 21:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('wushu', '0045_auto_20200419_2134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Simlecategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryName', models.CharField(blank=True, max_length=255, null=True)),
                ('compCategoryCompleted', models.BooleanField()),
                ('compOrder', models.IntegerField()),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('isDuilian', models.BooleanField()),
                ('kobilId', models.IntegerField()),
                ('operationDate', models.DateTimeField(auto_now_add=True)),
                ('playersOrdered', models.BooleanField()),
                ('recordCompleted', models.BooleanField()),
                ('competition', models.IntegerField()),
                ('area', models.IntegerField()),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.AlterField(
            model_name='level',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='license',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='taoluathlete',
            name='categori',
            field=models.ManyToManyField(to='wushu.Simlecategory'),
        ),
    ]
