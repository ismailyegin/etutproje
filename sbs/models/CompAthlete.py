from django.db import models

from sbs.models.Competition import Competition
from sbs.models.Weight import Weight
from sbs.models.CompCategory import CompCategory
from sbs.models.Athlete import Athlete


class CompAthlete(models.Model):
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    degree = models.IntegerField(default=0)
    kobilid = models.IntegerField(db_column='kobilId',default=0)  # Field name made lowercase.
    kop1 = models.IntegerField(default=0)
    kop1b = models.IntegerField(default=0)
    kop2 = models.IntegerField(default=0)
    kop2b = models.IntegerField(default=0)
    kop3 = models.IntegerField(default=0)
    kop3b = models.IntegerField(default=0)
    kopdegree = models.IntegerField(db_column='kopDegree',default=0)  # Field name made lowercase.
    kopkaldirissira = models.IntegerField(db_column='kopKaldirisSira',default=0)  # Field name made lowercase.
    kopsilktotal = models.IntegerField(db_column='kopSilkTotal',default=0)  # Field name made lowercase.
    koptotal = models.IntegerField(db_column='kopTotal',default=0)  # Field name made lowercase.
    lotno = models.IntegerField(db_column='lotNo',default=0)  # Field name made lowercase.
    operationdate = models.DateTimeField(db_column='operationDate', blank=True, null=True)  # Field name made lowercase.
    sessionno = models.IntegerField(db_column='sessionNo',default=0)  # Field name made lowercase.
    silk1 = models.IntegerField(default=0)
    silk1b = models.IntegerField(default=0)
    silk2 = models.IntegerField(default=0)
    silk2b = models.IntegerField(default=0)
    silk3 = models.IntegerField(default=0)
    silk3b = models.IntegerField(default=0)
    silkdegree = models.IntegerField(db_column='silkDegree',default=0)  # Field name made lowercase.
    silktotal = models.IntegerField(db_column='silkTotal',default=0)  # Field name made lowercase.
    total = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    athlete = models.ForeignKey(Athlete, models.DO_NOTHING, db_column='athlete', blank=True, null=True)
    compcategory = models.ForeignKey(CompCategory, models.DO_NOTHING, db_column='compCategory', blank=True, null=True)  # Field name made lowercase.
    sıklet = models.ForeignKey(Weight, models.DO_NOTHING, db_column='sıklet', blank=True, null=True)
    lastliftvalue = models.IntegerField(db_column='lastLiftValue', blank=True, null=True,default=0)  # Field name made lowercase.
    lastsilkliftvalue = models.IntegerField(db_column='lastSilkLiftValue', blank=True, null=True,default=0)  # Field name made lowercase.
    competition = models.ForeignKey(Competition, models.DO_NOTHING, db_column='competition', blank=True, null=True)

    class Meta:
        db_table = 'compathlete'
        managed = False