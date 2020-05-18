from django import forms
from django.forms import ModelForm

from sbs.models.EPDocument import EPDocument


class EPDocumentForm(ModelForm):
    class Meta:
        model = EPDocument

        fields = (
            'name',)
        labels = {
            'name': 'Doküman İsmi',


        }
        widgets = {
            'name':forms.ClearableFileInput(attrs={'multiple': True})





        }
