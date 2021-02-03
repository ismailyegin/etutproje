from django.db import models


class DirectoryMemberRole(models.Model):
    name = models.TextField(blank=False, null=False, verbose_name='Üye Rolü')
    kobilid = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return '%s ' % self.name


    class Meta:
        default_permissions = ()
