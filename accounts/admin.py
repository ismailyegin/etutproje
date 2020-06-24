from django.contrib import admin
from sbs.models.CategoryItem import CategoryItem
from rest_framework.authtoken.models import Token
from sbs.models.Athlete import Athlete
from sbs.models.Branch import Branch
from sbs.models.CategoryItem import CategoryItem
from sbs.models.Coach import Coach
from sbs.models.Communication import Communication
from sbs.models.Competition import Competition
from sbs.models.Judge import Judge
from sbs.models.Level import Level
from sbs.models.License import License
from sbs.models.Person import Person
from sbs.models.Punishment import Punishment
from sbs.models.SportsClub import SportsClub
from sbs.models.Menu import Menu
from sbs.models.MenuAdmin import MenuAdmin
from sbs.models.City import City
from sbs.models.Country import Country
from sbs.models.SportClubUser import SportClubUser
from sbs.models.ClubRole import ClubRole
from sbs.models.DirectoryCommission import DirectoryCommission
from sbs.models.DirectoryMemberRole import DirectoryMemberRole
from sbs.models.DirectoryMember import DirectoryMember
from sbs.models.BeltExam import BeltExam
from sbs.models.MenuPersonel import MenuPersonel
from sbs.models.MenuDirectory import MenuDirectory
from sbs.models.SimpleCategory import SimpleCategory
from sbs.models.CompAthlete import CompAthlete
from sbs.models.CompCategory import CompCategory
from sbs.models.GrupForReport import GrupForReport
from sbs.models.Weight import Weight
from sbs.models.EPProject import EPProject
from sbs.models.EPEmployee import EPEmployee
from sbs.models.EPRequirements import EPRequirements
from sbs.models.EPPhase import EPPhase
from sbs.models.EPOffer import EPOffer

# Register your models here.
admin.site.register(CategoryItem)
admin.site.register(EPPhase)
admin.site.register(EPOffer)
admin.site.register(EPRequirements)
admin.site.register(EPEmployee)
admin.site.register(EPProject)
admin.site.register(GrupForReport)
admin.site.register(MenuPersonel)
admin.site.register(DirectoryMemberRole)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Menu)
admin.site.register(Punishment)
admin.site.register(Person)
