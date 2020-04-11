from django import forms
from django.forms import ModelForm

from wushu.models.Level import Level



class VisaForm(ModelForm):

    class Meta:
        model =Level

        fields = (
             'dekont','branch')

        labels = {'branch':'Branş'}

        widgets = {


            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

        }
