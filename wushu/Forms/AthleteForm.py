from django import forms
from django.forms import ModelForm

from wushu.models import Athlete


class AthleteForm(ModelForm):
    class Meta:
        model = Athlete
