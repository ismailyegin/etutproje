from django import forms
from django.forms import ModelForm
from wushu.models.Simplecategory import Simlecategory


class SimplecategoryForm(ModelForm):
    class Meta:
        model = Simlecategory

        fields = ('categoryName',)

        labels = {'categoryName': 'İsim'}

        widgets = {

            'categoryName': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),

        }
