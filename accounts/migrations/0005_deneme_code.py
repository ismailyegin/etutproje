# Generated by Django 2.2.6 on 2020-04-11 09:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200411_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='deneme',
            name='code',
            field=models.UUIDField(default=uuid.UUID('c802a72b-4926-484f-8d09-ef4e9b267d7c'), editable=False),
        ),
    ]