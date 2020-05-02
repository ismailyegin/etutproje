from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm



class UserSearchForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active',)
        labels = {'first_name': 'Ad', 'last_name': 'Soyad'}
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Ad', 'value': ''}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Soyad'}),
            'email': forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Email'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'iCheck-helper'}),
            # 'password': forms.PasswordInput(attrs={'class': 'form-control ', 'placeholder': 'Şifre',}),

        }
