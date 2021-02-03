from django.db import models


class DirectoryCommission(models.Model):
    name = models.TextField(blank=False, null=False, verbose_name='Kurul Adı')
    kobilid = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions = ()
