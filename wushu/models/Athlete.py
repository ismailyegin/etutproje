from random import choices

from django.contrib.auth.models import User
from django.db import models

from wushu.models.License import License
from wushu.models.Level import Level
from wushu.models.Person import Person
from wushu.models.Communication import Communication


class Athlete(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    belts = models.ManyToManyField(Level)
    licenses = models.ManyToManyField(License)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)


    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        ordering = ['pk']
