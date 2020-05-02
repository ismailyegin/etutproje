from django import forms
from django.forms import ModelForm
from sbs.models.VisaSeminar import  VisaSeminar
class VisaSeminarForm(ModelForm):
    class Meta:
        model = VisaSeminar
        fields = (
            'name', 'startDate', 'finishDate', 'location', 'branch')
        labels = {'name': 'İsim', 'startDate': 'Başlangıç Tarihi', 'finishDate': 'Bitiş Tarihi',
                  'location': 'Yer', 'branch': 'Branş'}
        widgets = {
            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker2', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker4', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),

            'location': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),


        }
