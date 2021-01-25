from django.db import models


class GkiraBedeli(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)

    kiraTarihi = models.DateTimeField(null=False, blank=False)
    kiraBedeli = models.IntegerField(null=False, blank=False)
