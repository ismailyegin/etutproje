from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    notification = models.CharField(blank=True, null=True, max_length=200, verbose_name='Branş Adı')
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    users = models.ForeignKey(User, models.DO_NOTHING, blank=False, null=False)
    is_show = models.BooleanField(default=False)
    entityId = models.IntegerField()
    tableName = models.CharField(blank=True, null=True, max_length=120)

    def __str__(self):
        return '%s ' % self.notification

    class Meta:
        default_permissions = ()
