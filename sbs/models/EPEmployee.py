from random import choices

from django.contrib.auth.models import User
from django.db import models

from sbs.models import CategoryItem
from sbs.models.Employee import Employee


class EPEmployee(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    projectEmployeeTitle = models.ForeignKey(CategoryItem, on_delete=models.CASCADE,null=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,null=False)

    def __str__(self):
        return '%s %s %s %s' % (
        self.projectEmployeeTitle.name, ' - ', self.employee.user.first_name, self.user.last_name)

    class Meta:
        ordering = ['pk']
        default_permissions = ()
