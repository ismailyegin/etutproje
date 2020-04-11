from urllib import request

from django.db import models

from wushu.models.EnumFields import EnumFields


class CategoryItem(models.Model):
    name = models.CharField(blank=False, null=False, max_length=255)
    forWhichClazz = models.CharField(blank=False, null=False, max_length=255)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    branch = models.CharField(max_length=128, choices=EnumFields.BRANCH.value,null=True,blank=True,verbose_name='Seçiniz')
    isFirst = models.BooleanField()

    def __str__(self):
        return '%s %s %s' % (self.name,'-',self.branch)


    class Meta:
        default_permissions = ()
