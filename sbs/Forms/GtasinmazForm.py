from django import forms
from django.forms import ModelForm

from sbs.models.Gtasinmaz import Gtasinmaz
from sbs.models.Gkira import Gkira
from sbs.models.Gtahsis import Gtahsis
from sbs.models.Gkurum import Gkurum
from sbs.models.GTapu import GTapu
from sbs.models.Gteskilat import Gteskilat
from sbs.models.GkiraBedeli import GkiraBedeli


class GtasinmazForm(ModelForm):
    class Meta:
        model = Gtasinmaz

        fields = (
            'name', 'sirano', 'block', 'floor', 'mulkiyet', 'tkgmno', 'UsageArea', 'kurum', 'tahsis_durumu',
            'tasinmazinTuru')

        labels = {'name': 'İsim',
                  'sirano': 'Sıra numarası',
                  'block': 'Blok Adeti',
                  'floor': 'Kat Sayısı',
                  'mulkiyet': 'Mülkiyet',
                  'tkgmno': 'Tkgm numarası',
                  'UsageArea': 'Kullanılan Alan (m2) ',
                  'kurum': 'Binayı Kullanan Birim',
                  'tahsis_durumu': "Tahsis durumu",
                  'tasinmazinTuru': 'Taşınmazın Türü',

                  }

        widgets = {

            'kurum': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                         'style': 'width: 100%; ', 'required': 'required'}),

            'mulkiyet': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'required': 'required'}),
            'tahsis_durumu': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                 'style': 'width: 100%; ', 'required': 'required'}),
            'tasinmazinTuru': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                  'style': 'width: 100%; ', 'required': 'required'}),
            'sirano': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'tkgmno': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'floor': forms.TextInput(
                attrs={'class': 'form-control ', }),
            'block': forms.TextInput(
                attrs={'class': 'form-control ', }),
            'UsageArea': forms.TextInput(
                attrs={'class': 'form-control ', }),
            'name': forms.TextInput(
                attrs={'class': 'form-control ', }),

        }
