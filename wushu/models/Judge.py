from django.db import models

from wushu.models.Level import Level
from wushu.models.Punishment import Punishment
from wushu.models.Person import Person
from wushu.models.Communication import Communication
from django.contrib.auth.models import User


class Judge(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)


    class Meta:
        default_permissions = ()
