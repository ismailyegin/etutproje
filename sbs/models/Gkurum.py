from django.db import models


class Gkurum(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=120, null=True)

    def __str__(self):
        return '%s' % (self.name)
