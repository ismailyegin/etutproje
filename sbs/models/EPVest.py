from random import choices

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models



class EPVest(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    vestDate = models.DateField(blank=False, null=False)
    vest = models.CharField(blank=False, null=False, max_length=1000)



    class Meta:
        ordering = ['pk']
        default_permissions = ()