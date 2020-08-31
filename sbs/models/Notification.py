from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    notification = models.CharField(blank=True, null=True, max_length=120, verbose_name='Branş Adı')
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='user')
    is_show = models.BooleanField(default=False)
    url = models.CharField(max_length=120, null=True, blank=True)
    urlget = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self):
        return '%s ' % self.notification

    class Meta:
        default_permissions = ()
