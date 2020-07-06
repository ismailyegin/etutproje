from random import choices

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from sbs.models import CategoryItem
from sbs.models.Employee import Employee


class EPPhase(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    phaseDate = models.DateField(blank=False, null=False)
    definition = models.CharField(blank=False, null=False, max_length=1000)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 null=True, blank=True, on_delete=models.SET_NULL)

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)
    def __str__(self):
        return '%s ' % self.definition

    class Meta:
        ordering = ['pk']
        default_permissions = ()
