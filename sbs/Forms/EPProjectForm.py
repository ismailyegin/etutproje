from django import forms
from django.forms import ModelForm

from sbs.models import SportsClub, EPProject


class EPProjectForm(ModelForm):
    class Meta:
        model = EPProject

        fields = ('name',)
        labels = {
            'name': 'Adı'

        }
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'})

        }
