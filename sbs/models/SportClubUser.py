from django.contrib.auth.models import User
from django.db import models

from sbs.models import SportsClub
from sbs.models.Person import Person
from sbs.models.Communication import Communication
from sbs.models.ClubRole import ClubRole


class SportClubUser(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(ClubRole, on_delete=models.CASCADE, verbose_name='Üye Rolü')
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        default_permissions = ()


