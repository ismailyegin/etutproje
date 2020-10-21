from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from accounts.forms import LoginForm, PermForm
from accounts.models import Forgot

from sbs.Forms.PreRegidtrationForm import PreRegistrationForm

from django.contrib import auth, messages

from sbs import urls
from sbs.models import MenuPersonel, MenuDirectory, MenuAdmin, SportsClub, \
    SportClubUser
from sbs.models.PreRegistration import PreRegistration
from sbs.services import general_methods
from sbs.services.general_methods import show_urls

from sbs.Forms.ClubForm import ClubForm
from sbs.Forms.ClubRoleForm import ClubRoleForm
from sbs.Forms.CommunicationForm import CommunicationForm
from sbs.Forms.DisabledCommunicationForm import DisabledCommunicationForm
from sbs.Forms.DisabledPersonForm import DisabledPersonForm
from sbs.Forms.DisabledSportClubUserForm import DisabledSportClubUserForm
from sbs.Forms.DisabledUserForm import DisabledUserForm
from sbs.Forms.PersonForm import PersonForm
from sbs.Forms.SportClubUserForm import SportClubUserForm
from sbs.Forms.UserForm import UserForm

from django.contrib.auth.tokens import PasswordResetTokenGenerator


def index(request):
    return render(request, 'accounts/index.html')


def login(request):
    if request.user.is_authenticated is True:
        return redirect('sbs:admin')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # correct username and password login the user
            auth.login(request, user)

            log = general_methods.logwrite(request, " Giris yapti")



            if user.groups.all()[0].name == 'Yonetim':
                return redirect('sbs:federasyon')

            elif user.groups.all()[0].name == 'Admin':
                return redirect('sbs:admin')

            elif user.groups.all()[0].name == 'Personel':
                return redirect('sbs:personel')

            elif user.groups.all()[0].name == 'Teknik':
                return redirect('sbs:anasayfa-teknik')





            else:
                return redirect('accounts:logout')

        else:
            # eski kullanici olma ihtimaline göre sisteme girme yöntemi
            try:
                user = SportsClub.objects.get(username=request.POST.get('username'),
                                              password=request.POST.get('password'))
                if user is not None:
                    return redirect('accounts:newlogin', user.pk)
            except:
                print()

            messages.add_message(request, messages.SUCCESS, 'Mail Adresi Ve Şifre Uyumsuzluğu')
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')


# def forgot(request):
#     if request.method == 'POST':
#         mail = request.POST.get('username')
#         obj = User.objects.filter(username=mail)
#         if obj.count() != 0:
#             obj = obj[0]
#             password = User.objects.make_random_password()
#             obj.set_password(password)
#             # form.cleaned_data['password'] = make_password(form.cleaned_data['password'])
#
#             user = obj.save()
#             html_content = ''
#
#             subject, from_email, to = 'TWF Bilgi Sistemi Kullanıcı Bilgileri', 'no-reply@twf.gov.tr', obj.email
#             html_content = '<h2>Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.</h2>'
#             html_content = html_content+'<p> <strong>Site adresi:</strong> <a href="http://sbs.twf.gov.tr:81"></a>sbs.twf.gov.tr:81</p>'
#             html_content = html_content + '<p><strong>Kullanıcı Adı:</strong>' + obj.username + '</p>'
#             html_content = html_content + '<p><strong>Şifre:</strong>' + password + '</p>'
#             msg = EmailMultiAlternatives(subject, '', from_email, [to])
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()
#
#             messages.success(request, "Giriş bilgileriniz mail adresinize gönderildi. ")
#             return redirect("accounts:login")
#         else:
#             messages.warning(request, "Geçerli bir mail adresi giriniz.")
#             return redirect("accounts:forgot")
#
#     return render(request, 'registration/forgot-password.html')


def pre_registration(request):
    PreRegistrationform = PreRegistrationForm()

    if request.method == 'POST':
        PreRegistrationform = PreRegistrationForm(request.POST or None, request.FILES or None)

        if PreRegistrationform.is_valid():
            if User.objects.filter(email=PreRegistrationform.cleaned_data['email']).exists():
                messages.warning(request, 'Klup üyesi  mail adresi farklı bir kullanici tarafından kullanilmaktadır.')
                messages.warning(request, 'Lütfen farklı bir mail adresi giriniz.')
                return render(request, 'registration/cluppre-registration.html',
                              {'preRegistrationform': PreRegistrationform})
            else:
                PreRegistrationform.save()
                messages.success(request,
                                 "Başarili bir şekilde kayıt başvurunuz alındı Sistem onayından sonra girdiginiz mail adresinize gelen mail ile sisteme giris yapabilirsiniz.")

            # bildirim ve geçis sayfasi yap
            return redirect('accounts:login')

        else:
            messages.warning(request, "Alanlari kontrol ediniz")

    return render(request, 'registration/cluppre-registration.html', {'preRegistrationform': PreRegistrationform})


def pagelogout(request):
    log = "cikis yaptı "
    log = general_methods.logwrite(request, str(log))
    logout(request)
    print('çikis yaptı ')


    return redirect('accounts:login')


def mail(request):
    return redirect('accounts:login')


def groups(request):
    group = Group.objects.all()

    return render(request, 'permission/groups.html', {'groups': group})


@login_required
def permission(request, pk):
    general_methods.show_urls(urls.urlpatterns, 0)
    group = Group.objects.get(pk=pk)
    menu = ""
    ownMenu = ""

    groups = group.permissions.all()
    per = []
    menu2 = []

    for gr in groups:
        per.append(gr.codename)

    ownMenu = group.permissions.all()

    menu = Permission.objects.all()

    for men in menu:
        if men.codename in per:
            print("echo")
        else:
            menu2.append(men)

    return render(request, 'permission/izin-ayar.html',
                  {'menu': menu2, 'ownmenu': ownMenu, 'group': group})


@login_required
def permission_post(request):
    if request.POST:
        try:
            permissions = request.POST.getlist('values[]')
            group = Group.objects.get(pk=request.POST.get('group'))

            group.permissions.clear()
            group.save()
            if len(permissions) == 0:
                return JsonResponse({'status': 'Success', 'messages': 'Sınıf listesi boş'})
            else:
                for id in permissions:
                    perm = Permission.objects.get(pk=id)
                    group.permissions.add(perm)

            group.save()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Permission.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def updateUrlProfile(request):
    if request.method == 'GET':
        try:
            data = request.GET.get('query')
            gelen = Forgot.objects.get(uuid=data)
            user = gelen.user
            password_form = SetPasswordForm(user)
            if gelen.status == False:
                gelen.status = True
                gelen.save()
                return render(request, 'registration/newPassword.html',
                              {'password_form': password_form})

            else:
                return redirect('accounts:login')
        except:
            return redirect('accounts:login')

    if request.method == 'POST':
        try:
            gelen = Forgot.objects.get(uuid=request.GET.get('query'))
            password_form = SetPasswordForm(gelen.user, request.POST)
            user = gelen.user
            if password_form.is_valid():
                user.set_password(password_form.cleaned_data['new_password1'])
                user.save()
                # zaman kontrolüde yapilacak
                gelen.status = True
                messages.success(request, 'Şifre Başarıyla Güncellenmiştir.')

                return redirect('accounts:login')


            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')
                return render(request, 'registration/newPassword.html',
                              {'password_form': password_form})
        except:
            return redirect('accounts:login')

    return render(request, 'accounts/index.html')


def UserAllMail(request):
    for user in User.objects.all():
        fdk = Forgot(user=user, status=False)
        fdk.save()
        
        f = open("log.txt", "a")
        log = "şifre gönderildi"
        log = get_client_ip(request) + "    [" + datetime.today().strftime('%d-%m-%Y %H:%M') + "] " + str(
            user) + " " + log + " \n "
        f.write(log)
        f.close()

        html_content = ''
        subject, from_email, to = 'Etut Proje Bilgi Sistemi Kullanıcı Bilgileri', 'etutproje@kobiltek.com', mail
        html_content = '<h2>ADALET BAKANLIGI PROJE TAKİP  SİSTEMİ</h2>'
        html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
        # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/newpassword?query=' + str(
        #     fdk.uuid) + '">http://127.0.0.1:8000/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
        html_content = html_content + '<p> <strong>Yeni şifre oluşturma linki:</strong> <a href="http://www.kobiltek.com:81/etutproje/sbs/newpassword?query=' + str(
            fdk.uuid) + '">http://www.kobiltek.com:81/etutproje/sbs/profil-guncelle/?query=' + str(
            fdk.uuid) + '</p></a>'
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return redirect("accounts:login")







def forgot(request):
    if request.method == 'POST':
        mail = request.POST.get('username')
        obj = User.objects.filter(username=mail)
        print('ben geldim ')

        if obj.count() != 0:
            user = User.objects.get(username=mail)
            print(user)
            fdk = Forgot(user=user, status=False)
            fdk.save()

            log = general_methods.logwrite(request, " Yeni giris maili gönderildi")

            html_content = ''
            subject, from_email, to = 'Bilgi Sistemi Kullanıcı Bilgileri', 'etutproje@kobiltek.com', mail
            html_content = '<h2>ADALET BAKANLIGI PROJE TAKİP  SİSTEMİ</h2>'
            html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
            # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/newpassword?query=' + str(
            #     fdk.uuid) + '">http://127.0.0.1:8000/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
            html_content = html_content + '<p> <strong>Yeni şifre oluşturma linki:</strong> <a href="http://www.kobiltek.com:81/etutproje/sbs/newpassword?query=' + str(
                fdk.uuid) + '">http://www.kobiltek.com:81/etutproje/sbs/profil-guncelle/?query=' + str(
                fdk.uuid) + '</p></a>'

            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, "Giriş bilgileriniz mail adresinize gönderildi. ")
            return redirect("accounts:login")
        else:
            messages.warning(request, "Geçerli bir mail adresi giriniz.")
            return redirect("accounts:forgot")

    return render(request, 'registration/forgot-password.html')


def newlogin(request, pk):
    clup = SportsClub.objects.get(pk=pk)
    # clüp
    club_form = ClubForm(instance=clup)
    communication_formclup = CommunicationForm(instance=clup.communication)
    # klüp üyesi
    user_form = UserForm()
    person_form = PersonForm()
    communication_form = CommunicationForm()
    sportClubUser_form = SportClubUserForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST, request.FILES)
        communication_form = CommunicationForm(request.POST, request.FILES)
        sportClubUser_form = SportClubUserForm(request.POST)

        club_form = ClubForm(request.POST, request.FILES)
        communication_formclup = CommunicationForm(request.POST, request.FILES)

        if club_form.is_valid() and user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and sportClubUser_form.is_valid():
            clup.name = request.POST.get('name')
            clup.shortName = request.POST.get('shortName')
            clup.foundingDate = request.POST.get('foundingDate')
            clup.logo = request.POST.get('logo')
            clup.clubMail = request.POST.get('clubMail')
            clup.isFormal = request.POST.get('isFormal')

            communication = communication_formclup.save(commit=False)
            communication.save()
            clup.communication = communication
            clup.save()

            messages.success(request, 'Bilgileriniz Başarıyla Güncellenmiştir.')

            user = User()
            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            group = Group.objects.get(name='KulupUye')
            user.save()
            user.groups.add(group)
            user.save()

            person = person_form.save(commit=False)
            communication = communication_form.save(commit=False)
            person.save()
            communication.save()

            club_person = SportClubUser(
                user=user, person=person, communication=communication,
                role=sportClubUser_form.cleaned_data['role'],

            )

            club_person.save()

            fdk = Forgot(user=user, status=False)
            fdk.save()

            html_content = ''
            html_content = ''
            subject, from_email, to = 'Bilgi Sistemi Kullanıcı Bilgileri', 'etutproje@kobiltek.com', mail
            html_content = '<h2>ADALET BAKANLIGI PROJE TAKİP  SİSTEMİ</h2>'
            html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
            # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/newpassword?query=' + str(
            #     fdk.uuid) + '">http://127.0.0.1:8000/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
            html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://kobiltek.com:81/etutproje/newpassword?query=' + str(
                fdk.uuid) + '">http://kobiltek.com:81/etutproje/sbs/profil-guncelle/?query=' + str(
                fdk.uuid) + '</p></a>'

            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            clup.clubUser.add(club_person)
            clup.dataAccessControl = True
            clup.save()
            messages.success(request, 'Mail adresinize gelen link ile sisteme giriş yapabilirsiniz.')
            return redirect("accounts:login")

        # try:
        #
        #
        # except:
        #     messages.warning(request, 'Lütfen Yeniden Deneyiniz')
        #     return redirect("accounts:login")

    return render(request, 'registration/newlogin.html',
                  {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form,
                   'sportClubUser_form': sportClubUser_form, 'club_form': club_form,
                   'communication_formclup': communication_formclup})
