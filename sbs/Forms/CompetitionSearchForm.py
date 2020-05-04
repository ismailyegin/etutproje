from django import forms
from django.forms import ModelForm

from sbs.models import  Competition


class CompetitionSearchForm(ModelForm):



    class Meta:
        model = Competition

        fields = (
            'name', 'startDate', 'finishDate','compType','compGeneralType')

        labels = {'name': 'İsim', 'startDate': 'Başlangıç Tarihi', 'finishDate': 'Bitiş Tarihi', 'compType': 'Türü', 'compGeneralType': 'Genel Türü'}

        widgets = {

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker5', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),

            'name': forms.TextInput(attrs={'class': 'form-control'}),

            'compType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),
            'compGeneralType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; '}),



        }
