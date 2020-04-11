from django.db import models

from wushu.models.SportClubUser import SportClubUser
from wushu.models.Coach import Coach
from wushu.models.Communication import Communication


class SportsClub(models.Model):
    IsFormal = (
        (True, 'Spor Kulubü'),
        (False, 'Diger(Özel Salon-Dojo-Sportif Dernek)'),
    )

    name = models.CharField(blank=True, null=True, max_length=120)
    shortName = models.CharField(blank=True, null=True, max_length=120)
    foundingDate = models.CharField(blank=True, null=True, max_length=120)
    clubMail = models.CharField(blank=True, null=True, max_length=120)
    logo = models.ImageField(upload_to='club/', null=True, blank=True, verbose_name='Kulüp Logo')
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    coachs = models.ManyToManyField(Coach)
    isFormal = models.BooleanField(default=True,choices=IsFormal)
    clubUser = models.ManyToManyField(SportClubUser)

    def __str__(self):
        return '%s %s %s' % (self.shortName, '-', self.name)

    class Meta:
        default_permissions = ()
