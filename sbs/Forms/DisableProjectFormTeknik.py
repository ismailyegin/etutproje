from django import forms
from django.forms import ModelForm

from sbs.models import SportsClub, EPProject


class DisableProjectFormTeknik(ModelForm):
    class Meta:
        model = EPProject

        fields = ('name', 'butceCinsi', 'butceYili', 'projeCinsi', 'ihaleTarihi',  'sozlesmeTarihi', 'isSUresi',
                  'isBitimTarihi', 'city','sorumlu','aistart','aifinish','karakteristik','projectStatus')
        labels = {
            'name': 'Proje Tanımı',
            'butceCinsi': 'Yatırım Programı ',
            'butceYili': 'Bütçe Yılı',
            'projeCinsi': 'Proje Cinsi',
            'ihaleTarihi': 'İhale Tarihi',
            'sozlesmeTarihi': 'Sözleşme Tarihi',
            'isSUresi': 'İşin Süresi (Gün)',
            'isBitimTarihi': 'İş Bitim Tarihi',
            'city': 'İl',
            'sorumlu':'Proje Sorumlusu',
            'aistart':'Alım İşinin Başlangıç Tarihi',
            'aifinish':'Alım İşinin Bitiş Tarihi',
            'karakteristik':'Karakteristik',
            'projectStatus':'Projenin Durumu',


        }
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required','readonly': 'readonly'}),
            'butceCinsi': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required','readonly': 'readonly'}),
            'butceYili': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required','readonly': 'readonly'}),

            'projeCinsi': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required','readonly': 'readonly'}),
            'karakteristik': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required','readonly': 'readonly'}),

            'projectStatus': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required','readonly': 'readonly'}),

            # 'pattern': '"^\$\d{1.3}(.\d{3})*(\,\d+)?$"', 'data-type': 'currency'
            # 'insaatAlani': forms.TextInput(
            #     attrs={'class': 'form-control ',}),
            'ihaleTarihi': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datemask7', 'autocomplete': 'on',
                       'onkeydown': 'return true','readonly': 'readonly'}),
            'sozlesmeTarihi': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datemask5', 'autocomplete': 'on',
                       'onkeydown': 'return true','readonly': 'readonly'}),
            'isSUresi': forms.TextInput(attrs={'class': 'form-control ', 'id': 'number','readonly': 'readonly'}),
            'isBitimTarihi': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datemask6', 'autocomplete': 'on',
                       'onkeydown': 'return true','readonly': 'readonly'}),
            'city': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required','readonly': 'readonly'}),
            'sorumlu': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required','readonly': 'readonly'}),
            'aistart': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'autocomplete': 'on',
                       'onkeydown': 'return true','readonly': 'readonly'}),
            'aifinish': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'autocomplete': 'on',
                       'onkeydown': 'return true','readonly': 'readonly'}),

        }
