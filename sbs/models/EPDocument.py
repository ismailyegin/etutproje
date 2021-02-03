from django.db import models


class EPDocument(models.Model):

    name=models.FileField(upload_to='document/', null=True, blank=True, verbose_name='Document')
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    kobilid = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return '%s ' % self.name