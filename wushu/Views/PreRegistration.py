from itertools import product

from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from wushu.Forms.BeltExamForm import BeltExamForm
from wushu.Forms.ClubForm import ClubForm
from wushu.Forms.ClubRoleForm import ClubRoleForm
from wushu.Forms.CommunicationForm import CommunicationForm
from wushu.Forms.DisabledCommunicationForm import DisabledCommunicationForm
from wushu.Forms.DisabledPersonForm import DisabledPersonForm
from wushu.Forms.DisabledSportClubUserForm import DisabledSportClubUserForm
from wushu.Forms.DisabledUserForm import DisabledUserForm
from wushu.Forms.PersonForm import PersonForm
from wushu.Forms.SportClubUserForm import SportClubUserForm
from wushu.Forms.UserForm import UserForm
from wushu.Forms.PreRegidtrationForm import PreRegistrationForm
from wushu.Forms.UserSearchForm import UserSearchForm
from wushu.models import SportsClub, SportClubUser, Communication, Person, BeltExam, Athlete, Coach, Level, CategoryItem
from wushu.models.ClubRole import ClubRole
from wushu.models.EnumFields import EnumFields
from wushu.models.PreRegistration import PreRegistration
from wushu.services import general_methods
import datetime


from django.contrib.auth.models import Group, Permission, User

def update_preRegistration(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    veri=PreRegistration.objects.get(pk=pk)
    form=PreRegistrationForm(request.POST or None, instance=veri)
    if request.method == 'POST':
        if form.is_valid():
            email=form.cleaned_data['email']
            if User.objects.filter(email=email).exists() and veri.email!=email :
                messages.warning(request, 'Bu mail adresi farklı bir kullanici tarafından kullanilmaktadır xxx')
                return render(request, 'kulup/kulup-basvuru-duzenle.html',
                              {'preRegistrationform': form, })
            form.save()
            messages.success(request,'Basarili bir şekilde kaydedildi ')
            return redirect('wushu:basvuru-listesi')
        else:
            messages.warning(request,'Alanlari kontrol ediniz')
    return render(request, 'kulup/kulup-basvuru-duzenle.html',
                  {'preRegistrationform': form,})



@login_required
def rejected_preRegistration(request,pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    print('geldim ben pk= ',pk)
    messages.success(request, 'Öneri reddedildi ')
    veri=PreRegistration.objects.get(pk=pk)
    veri.status=PreRegistration.DENIED
    veri.save()
    prepegidtration=PreRegistration.objects.all()
    return render(request, 'kulup/kulupBasvuru.html',
                  {'prepegidtration': prepegidtration })



@login_required
def approve_preRegistration(request,pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    basvuru=PreRegistration.objects.get(pk=pk)
    if basvuru.status!=PreRegistration.APPROVED:
        if not (User.objects.filter(email=basvuru.email).exists()):
            # user kaydet
            try:
                user = User()
                user.username = basvuru.email
                user.first_name = basvuru.first_name
                user.last_name = basvuru.last_name
                user.email = basvuru.email
                user.is_active = basvuru.is_active
                user.is_staff = basvuru.is_staff
                group = Group.objects.get(name='KulupUye')
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()
                user.groups.add(group)
                user.save()
            except:
                messages.warning(request, ' Kullanici eklenmedi ')

            try:
                # person kaydet
                person = Person()
                person.tc = basvuru.tc
                person.height = basvuru.height
                person.weight = basvuru.weight
                person.birthplace = basvuru.birthplace
                person.motherName = basvuru.motherName
                person.fatherName = basvuru.fatherName
                person.profileImage = basvuru.profileImage
                person.birthDate = basvuru.birthDate
                person.bloodType = basvuru.bloodType
                person.gender = basvuru.gender
                person.save()

            except:
                messages.warning(request, ' Kullanici eklenmedi ')

            try:
                # Communication kaydet
                com = Communication()
                com.postalCode = basvuru.postalCode
                com.phoneNumber = basvuru.phoneNumber
                com.phoneNumber2 = basvuru.phoneNumber2
                com.address = basvuru.address
                com.city = basvuru.city
                com.country = basvuru.country
                com.save()

                Sportclup = SportClubUser()
                Sportclup.user = user
                Sportclup.person = person
                Sportclup.communication = com
                Sportclup.role = basvuru.role
                Sportclup.save()

                comclup = Communication()
                comclup.postalCode = basvuru.clubpostalCode
                comclup.phoneNumber = basvuru.clubphoneNumber
                comclup.phoneNumber2 = basvuru.clubphoneNumber2
                comclup.address = basvuru.clubaddress
                comclup.city = basvuru.clubcity
                comclup.country = basvuru.clubcountry
                comclup.save()

                # SportClup
                clup = SportsClub()
                clup.name = basvuru.name
                clup.shortName = basvuru.shortName
                clup.foundingDate = basvuru.foundingDate
                clup.clubMail = basvuru.clubMail
                clup.logo = basvuru.logo
                clup.isFormal = basvuru.isFormal
                clup.communication = comclup
                clup.save()
                clup.clubUser.add(Sportclup)
                clup.save()

                basvuru.status = PreRegistration.APPROVED
                basvuru.save()
            except:
                messages.success(request, 'Klüp ve iletisim kaydedilemedi')

            try:
                subject, from_email, to = 'WUSHU - Kulüp Üye Bilgi Sistemi Kullanıcı Giriş Bilgileri', 'no-reply@twf.gov.tr', user.email
                text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
                html_content = '<p> <strong>Site adresi: </strong> <a href="http://sbs.twf.gov.tr:81/"></a>sbs.twf.gov.tr:81</p>'
                html_content = html_content + '<p><strong>Kullanıcı Adı:  </strong>' + user.username + '</p>'
                html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                messages.success(request, 'Kullanici kaydedildi ve şifresi  gönderildi.')
            except:
                messages.warning(request, 'mail gönderilemedi')


        else:
            messages.warning(request, 'Mail adresi sistem de kayıtlıdır. ')
    else:
        messages.warning(request,'Bu basvuru sisteme kaydedilmistir.')

    prepegidtration=PreRegistration.objects.all()
    return render(request, 'kulup/kulupBasvuru.html',
                  {'prepegidtration': prepegidtration })




@login_required
def return_preRegistration(request):
    perm = general_methods.control_access(request)


    if not perm:
        logout(request)
        return redirect('accounts:login')

    prepegidtration=PreRegistration.objects.all()
    return render(request, 'kulup/kulupBasvuru.html',
                  {'prepegidtration': prepegidtration })

