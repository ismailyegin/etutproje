from django.db import models
from sbs.models.CategoryItem import CategoryItem
from sbs.models.Company import Company


class SubCompany(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, verbose_name='firma', related_name='firma',
                                null=True, blank=True)
    jopDescription = models.ForeignKey(CategoryItem, on_delete=models.SET_NULL, verbose_name='item',
                                       related_name='item',
                                       null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.company.name)

    class Meta:
        ordering = ['pk']
