from django import forms
from django.forms import ModelForm

from sbs.models import Gtasinmaz, GkiraBedeli, Gteskilat, GTapu, Gkurum, Gkira, Gtahsis


class GradeFormReferee(ModelForm):
    class Meta:
        model = Gtasinmaz

        fields = (
            'name', 'sirano', 'block', 'floor', 'mulkiyet',)

        labels = {'startDate': 'Hak Kazanma Tarihi', 'branch': 'Branş'}

        widgets = {

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker4', 'autocomplete': 'off',
                       'onkeydown': 'return false'}),
            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

        }
