
from django.db import models

from wushu.models.Athlete import Athlete
from wushu.models.Competition import Competition


class simlecategory(models.Model):
    categoryName = models.CharField(max_length=255, null=True, blank=True)
    compCategoryCompleted=models.BooleanField()
    compOrder=models.IntegerField()
    creationDate=models.DateTimeField(auto_now_add=True)
    isDuilian=models.BooleanField()
    kobilId=models.IntegerField()
    operationDate=models.DateTimeField(auto_now_add=True)
    playersOrdered=models.BooleanField()
    recordCompleted=models.BooleanField()
    competition=models.IntegerField()
    area=models.IntegerField()




    def __str__(self):
        return '%s' (self.categoryName)

    class Meta:
        default_permissions = ()