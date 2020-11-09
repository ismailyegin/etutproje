from django import forms
from django.forms import ModelForm

from sbs.models import SportsClub, EPProject


class EPProjectSorumluForm(ModelForm):
    class Meta:
        model = EPProject

        fields = ('name', 'butceCinsi', 'butceYili', 'projeCinsi', 'ihaleTarihi',  'sozlesmeTarihi', 'isSUresi',
                  'isBitimTarihi', 'city', 'aistart', 'aifinish', 'karakteristik', 'projectStatus', 'company')
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
            'aistart':'Alım İşinin Başlangıç Tarihi',
            'aifinish':'Alım İşinin Bitiş Tarihi',
            'karakteristik':'Karakteristik',
            'projectStatus':'Projenin Durumu',
            'company': 'Firma',


        }
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'butceCinsi': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%; ', 'required': 'required'}),
            'butceYili': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker5', 'autocomplete': 'on',
                       'onkeydown': 'return true', 'required': 'required'}),
            'projeCinsi': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%;', 'required': 'required'}),
            'karakteristik': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%; ', 'required': 'required'}),

            'projectStatus': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                 'style': 'width: 100%; ', 'required': 'required'}),

            # 'pattern': '"^\$\d{1.3}(.\d{3})*(\,\d+)?$"', 'data-type': 'currency'
            # 'insaatAlani': forms.TextInput(
            #     attrs={'class': 'form-control ',}),
            'ihaleTarihi': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datemask7', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'sozlesmeTarihi': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datemask5', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'isSUresi': forms.TextInput(attrs={'class': 'form-control ', 'id': 'number'}),
            'isBitimTarihi': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datemask6', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;','id':'sehir', 'required': 'required'}),
            'aistart': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'aifinish': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),

        }
