from django.db import models
from sbs.models.City import City


class Town(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name='İlçe')
    cityId = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl', db_column='cityId')
    kobilid = models.IntegerField(db_column='kobilId')
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.name

    def save(self, force_insert=False, force_update=False):
        self.name = self.name.upper()
        super(Town, self).save(force_insert, force_update)

    class Meta:
        default_permissions = ()
        db_table = 'town'
        managed = False




