
from django.db import models

from wushu.models.Athlete import Athlete
from wushu.models.Competition import Competition
from wushu.models.Simplecategory import Simlecategory

class TaoluAthlete(models.Model):
    athlete = models.OneToOneField(Athlete, on_delete=models.CASCADE)
    competition = models.OneToOneField(Competition, on_delete=models.CASCADE)
    categori = models.ManyToManyField(Simlecategory)

    def __str__(self):
        return '%s %s' % (self.athlete.user.first_name, self.athlete.user.last_name)

    class Meta:
        default_permissions = ()
