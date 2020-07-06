from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from sbs.models.CategoryItem import CategoryItem



class UserSearchForm(ModelForm):
    workDefinition = forms.ModelChoiceField(queryset=CategoryItem.objects.filter(forWhichClazz="EMPLOYEE_WORKDEFINITION"),
        to_field_name='name',
        empty_label="Seçiniz",
        label="Unvan",
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control select2 select2-hidden-accessible',
                   'style': 'width: 100%; '}))

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
