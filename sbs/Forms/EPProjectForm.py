from django import forms
from django.forms import ModelForm

from sbs.models import SportsClub, EPProject


class EPProjectForm(ModelForm):
    class Meta:
        model = EPProject

        fields = ('name', 'butceCinsi', 'butceYili', 'projeCinsi', 'arsaAlani', 'insaatAlani', 'tahminiOdenekTutari',
                  'yaklasikMaliyet', 'ihaleTarihi', 'sozlesmeBedeli', 'sozlesmeTarihi', 'isSUresi',
                  'isBitimTarihi', 'city',)
        labels = {
            'name': 'Proje Tanımı',
            'butceCinsi': 'Bütçe Cinsi',
            'butceYili': 'Bütçe Yılı',
            'projeCinsi': 'Proje Cinsi',
            'arsaAlani': 'Arsa Alanı (m2)',
            'insaatAlani': 'İnşaat Alanı (m2)',
            'tahminiOdenekTutari': 'Tahmini Ödenek Tutarı (₺)',
            'yaklasikMaliyet': 'Yaklaşık Maliyet (₺)',
            'ihaleTarihi': 'İhale Tarihi',
            'sozlesmeBedeli': 'Sözleşme Bedeli (₺)',
            'sozlesmeTarihi': 'Sözleşme Tarihi',
            'isSUresi': 'İşin Süresi (Gün)',
            'isBitimTarihi': 'İş Bitim Tarihi',
            'city': 'İl',

        }
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'butceCinsi': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%; '}),
            'butceYili': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker5', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'projeCinsi': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%; '}),
            'arsaAlani': forms.TextInput(
                attrs={'class': 'form-control '}),
            'insaatAlani': forms.TextInput(
                attrs={'class': 'form-control '}),
            'tahminiOdenekTutari': forms.TextInput(
                attrs={'class': 'form-control '}),
            'yaklasikMaliyet': forms.TextInput(
                attrs={'class': 'form-control '}),
            'ihaleTarihi': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datemask7', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'sozlesmeBedeli': forms.TextInput(
                attrs={'class': 'form-control ', }),
            'sozlesmeTarihi': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datemask5', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'isSUresi': forms.TextInput(attrs={'class': 'form-control ','id':'number'}),
            'isBitimTarihi': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datemask6', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),

        }
