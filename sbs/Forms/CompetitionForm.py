from django import forms
from django.forms import ModelForm

from sbs.models import  Competition


class CompetitionForm(ModelForm):



    class Meta:
        model = Competition

        fields = (
            'name', 'startDate', 'finishDate','compType','compGeneralType','eventPlace','eventDate','juryCount','registerStartDate','registerFinishDate')

        labels = {'name': 'İsim', 'startDate': 'Başlangıç Tarihi', 'finishDate': 'Bitiş Tarihi', 'compType': 'Türü', 'compGeneralType': 'Genel Türü',
                  'eventPlace':'Etkinlik Yeri','eventDate':'Etkinlik tarihi','juryCount':'Juri Sayisi','registerStartDate':'Ön Kayıt Başlangıç Tarihi',
                  'registerFinishDate':'Ön Kayıt Bitiş Tarihi'}

        widgets = {



            'juryCount': forms.NumberInput(attrs={'class': 'form-control'}),

            'registerStartDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6',  'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'registerFinishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'eventDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'eventPlace': forms.TextInput(attrs={'class': 'form-control'}),

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker2', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),

            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker4', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),

            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),

            'compType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),
            'compGeneralType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; '}),



        }
