from django import forms
from django.forms import ModelForm

from sbs.models import SportsClub, EPProject


class EPProjectForm(ModelForm):
    class Meta:
        model = EPProject

        fields = ('name','mimar','insaatMuhStatik','makineMuh','elektrikMuh','insaatMuhYaklasik',
                  'elektronikMuh','jeofizikMuh','cevreMuh','peyzajMimari','musahitMuh',
                  'butceCinsi','butceYili','projeCinsi','arsaAlani','insaatAlani','tahminiOdenekTutari',
                  'yaklasikMaliyet','ihaleTarihi','sozlesmeBedeli','sozlesmeTarihi','isSUresi',
                  'isBitimTarihi','city',)
        labels = {
            'name': 'Proje Tanımı',
            'mimar': 'Mimar',
            'insaatMuhStatik': 'İnşaat Mühendisi (Statik)',
            'makineMuh': 'Makine Mühendisi',
            'elektrikMuh': 'Elektrik Mühendisi',
            'insaatMuhYaklasik': 'İnşaat Mühendisi (Yaklaşık)',
            'elektronikMuh': 'Elektronik Mühendisi',
            'jeofizikMuh': 'Jeofizik Mühendisi',
            'cevreMuh': 'Çevre Mühendisi',
            'peyzajMimari': 'Peyzaj Mimarı',
            'musahitMuh': 'Müşahit Mühendis',
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
            'isSUresi': 'İşin Süresi',
            'isBitimTarihi': 'İş Bitim Tarihi',
            'city': 'İl',



        }
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'mimar': forms.TextInput(attrs={'class': 'form-control '}),
            'insaatMuhStatik': forms.TextInput(attrs={'class': 'form-control '}),
            'makineMuh': forms.TextInput(attrs={'class': 'form-control '}),
            'elektrikMuh': forms.TextInput(attrs={'class': 'form-control '}),
            'insaatMuhYaklasik': forms.TextInput(attrs={'class': 'form-control '}),
            'elektronikMuh': forms.TextInput(attrs={'class': 'form-control '}),
            'jeofizikMuh': forms.TextInput(attrs={'class': 'form-control '}),
            'cevreMuh': forms.TextInput(attrs={'class': 'form-control '}),
            'peyzajMimari': forms.TextInput(attrs={'class': 'form-control '}),
            'musahitMuh': forms.TextInput(attrs={'class': 'form-control '}),
            'butceCinsi': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; '}),
            'butceYili': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker5', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'projeCinsi': forms.TextInput(attrs={'class': 'form-control '}),
            'arsaAlani': forms.TextInput(attrs={'class': 'form-control '}),
            'insaatAlani': forms.TextInput(attrs={'class': 'form-control '}),
            'tahminiOdenekTutari': forms.TextInput(attrs={'class': 'form-control '}),
            'yaklasikMaliyet': forms.TextInput(attrs={'class': 'form-control '}),
            'ihaleTarihi': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'sozlesmeBedeli': forms.TextInput(attrs={'class': 'form-control '}),
            'sozlesmeTarihi': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker2', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'isSUresi': forms.TextInput(attrs={'class': 'form-control '}),
            'isBitimTarihi': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker3', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),



        }
