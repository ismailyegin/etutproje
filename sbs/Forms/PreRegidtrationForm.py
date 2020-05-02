from django import forms
from django.forms import ModelForm
from sbs.models import SportClubUser

from sbs.models.PreRegistration import PreRegistration


class PreRegistrationForm(ModelForm):

    class Meta:
        model = PreRegistration

        fields = (
            'tc', 'profileImage', 'height', 'weight', 'birthDate', 'bloodType', 'gender', 'birthplace', 'motherName','fatherName', 'first_name', 'last_name', 'email', 'is_active','phoneNumber', 'address', 'postalCode', 'phoneNumber2', 'city', 'country', 'name', 'shortName', 'foundingDate', 'logo', 'clubMail', 'isFormal',
            'clubphoneNumber', 'clubaddress', 'clubpostalCode', 'clubphoneNumber2', 'clubcity', 'clubcountry','dekont','petition','role')
        labels = {'tc': 'T.C.', 'gender': 'Cinsiyet', 'first_name': 'Ad', 'last_name': 'Soyad', 'email': 'Email','phoneNumber': 'Cep Telefonu', 'phoneNumber2': 'Sabit Telefon', 'postalCode': 'Posta Kodu',
                  'city': 'İl', 'country': 'Ülke','name': 'Adı','shortName': 'Kısa Adı','foundingDate': 'Kuruluş Tarihi','clubMail': 'Email','isFormal' : 'Kulüp Türü','role': 'Kulüp Rolü','clubphoneNumber':'Cep Telefonu','clubphoneNumber2':'Sabit Telefon', }

        widgets = {
            'isFormal':forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; ', 'required': 'required'}),
            'role': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; ', 'required': 'required'}),

            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'shortName': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),

            'clubMail': forms.TextInput(attrs={'class': 'form-control'}),

            'foundingDate': forms.DateInput(attrs={'class': 'form-control  pull-right', 'id': 'datepicker2', 'autocomplete': 'off','onkeydown': 'return false', 'required': 'required'}),

            'clubaddress': forms.Textarea(attrs={'class': 'form-control ', 'rows': '2'}),

            'clubphoneNumber': forms.TextInput(attrs={'class': 'form-control '}),

            'clubphoneNumber2': forms.TextInput(attrs={'class': 'form-control '}),

            'clubpostalCode': forms.TextInput(attrs={'class': 'form-control '}),

            'clubcity': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible', 'style': 'width: 100%;', 'required': 'required'}),

            'clubcountry': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible','style': 'width: 100%;', 'required': 'required'}),

            'address': forms.Textarea(
                attrs={'class': 'form-control ', 'rows': '2'}),

            'phoneNumber': forms.TextInput(attrs={'class': 'form-control '}),

            'phoneNumber2': forms.TextInput(attrs={'class': 'form-control '}),

            'postalCode': forms.TextInput(attrs={'class': 'form-control '}),

            'city': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),

            'country': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;', 'required': 'required'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'email': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'is_active': forms.CheckboxInput(attrs={'class': 'iCheck-helper'}),

            'tc': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'height': forms.TextInput(attrs={'class': 'form-control'}),

            'weight': forms.TextInput(attrs={'class': 'form-control'}),

            'birthplace': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),

            'motherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),

            'fatherName': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),

            'bloodType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%; '}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),


        }





