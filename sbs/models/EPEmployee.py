from random import choices

from django.contrib.auth.models import User
from django.db import models

from sbs.models import CategoryItem
from sbs.models.Employee import Employee


class EPEmployee(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    projectEmployeeTitle = models.ForeignKey(CategoryItem, on_delete=models.CASCADE,null=False)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING,null=False)

    def __str__(self):
        return '%s ' % self.employee


    class Meta:
        ordering = ['pk']
        default_permissions = ()
