from random import choices

from django.contrib.auth.models import User
from django.db import models

from sbs.models import CategoryItem
from sbs.models.Employee import Employee


class EPRequirements(models.Model):
    amount = models.IntegerField(null=False, blank=False, default=0)
    definition = models.CharField(blank=False, null=False, max_length=255)
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['pk']
        default_permissions = ()
