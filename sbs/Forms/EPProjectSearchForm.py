
from django import forms
from django.forms import ModelForm

from sbs.models import SportsClub, EPProject


class EPProjectSearchForm(ModelForm):
    class Meta:
        model = EPProject

        fields = ( 'butceCinsi', 'butceYili', 'projeCinsi', 'city','projectStatus','name','karakteristik')
        labels = {
            'name': 'Proje Tanımı',
            'butceCinsi': 'Yatırım Programı ',
            'butceYili': 'Bütçe Yılı',
            'projeCinsi': 'Proje Cinsi',

            'city': 'İl',

            'projectStatus':'Projenin Durumu',
            'karakteristik':'karakteristik',


        }
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control '}),

            'karakteristik': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%; '}),
            'butceCinsi': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%; '}),
            'butceYili': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker5', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'projeCinsi': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%;'}),


            'projectStatus': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                 'style': 'width: 100%; '}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible','style': 'width: 100%;'})


        }
    def __init__(self, *args, **kwargs):
            super(EPProjectSearchForm, self).__init__(*args, **kwargs)
            self.fields['butceCinsi'].required = False
            self.fields['butceYili'].required = False
            self.fields['projeCinsi'].required = False
            self.fields['projectStatus'].required = False
            self.fields['city'].required = False
            self.fields['name'].required = False
            self.fields['karakteristik'].required = False
            self.fields['karakteristik'].default=None
