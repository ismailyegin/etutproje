from builtins import print, set, property, int
from datetime import timedelta, datetime
from operator import attrgetter
from os import name

from django.db.models.functions import Lower

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from sbs.Forms.BeltForm import BeltForm
from sbs.Forms.CategoryItemForm import CategoryItemForm
from sbs.Forms.CommunicationForm import CommunicationForm
from sbs.Forms.DisabledCommunicationForm import DisabledCommunicationForm
from sbs.Forms.DisabledPersonForm import DisabledPersonForm
from sbs.Forms.DisabledUserForm import DisabledUserForm
from sbs.Forms.LicenseForm import LicenseForm
from sbs.Forms.UserForm import UserForm
from sbs.Forms.PersonForm import PersonForm
from sbs.Forms.UserSearchForm import UserSearchForm
from sbs.Forms.SearchClupForm import SearchClupForm
from sbs.models import Athlete, CategoryItem, Person, Communication, License, SportClubUser, SportsClub
from sbs.models.EnumFields import EnumFields
from sbs.models.Level import Level
from sbs.services import general_methods

# page
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from sbs.models.simplecategory import simlecategory

@login_required
def return_add_athlete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = UserForm()
    person_form = PersonForm()

    communication_form = CommunicationForm()

    # lisans ekleme baslangıç
    # klüp üyesi sadece kendi klüplerini görebiliyor
    user = request.user
    license_form = LicenseForm(request.POST, request.FILES or None)

    if user.groups.filter(name='KulupUye'):
        sc_user = SportClubUser.objects.get(user=user)
        clubs = SportsClub.objects.filter(clubUser=sc_user)

        clubsPk = []
        for club in clubs:
            clubsPk.append(club.pk)
        license_form.fields['sportsClub'].queryset = SportsClub.objects.filter(id__in=clubsPk)

    elif user.groups.filter(name__in=['Yonetim', 'Admin']):
        license_form.fields['sportsClub'].queryset = SportsClub.objects.all()

    # lisan ekleme son alani bu alanlar sadece form bileselerinin sisteme gidebilmesi icin post ile gelen veride gene ayni şekilde  karşılama ve kaydetme islemi yapilacak

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST, request.FILES)
        communication_form = CommunicationForm(request.POST)
        license_form = LicenseForm(request.POST, request.FILES or None)


        if user_form.is_valid() and person_form.is_valid() and license_form.is_valid() and communication_form.is_valid():
            user = User()
            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name'].upper()
            user.last_name = user_form.cleaned_data['last_name'].upper()
            user.email = user_form.cleaned_data['email']
            group = Group.objects.get(name='Sporcu')
            password = User.objects.make_random_password()
            user.set_password(password)
            user.is_active = False
            user.save()

            user.groups.add(group)
            user.save()

            person = person_form.save(commit=False)
            communication = communication_form.save(commit=False)
            person.save()
            communication.save()

            athlete = Athlete(
                user=user, person=person, communication=communication,
            )

            # lisans kaydedildi  kakydetmeden id degeri alamayacagi icin önce kaydedip sonra ekleme islemi yaptık
            license = license_form.save()
            athlete.save()
            athlete.licenses.add(license)

            # subject, from_email, to = 'WUSHU - Sporcu Bilgi Sistemi Kullanıcı Giriş Bilgileri', 'ik@oxityazilim.com', user.email
            # text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            # html_content = '<p> <strong>Site adresi: </strong> <a href="https://www.twf.gov.tr/"></a>https://www.twf.gov.tr/</p>'
            # html_content = html_content + '<p><strong>Kullanıcı Adı:  </strong>' + user.username + '</p>'
            # html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            messages.success(request, 'Sporcu Başarıyla Kayıt Edilmiştir.')

            return redirect('sbs:sporcular')

        else:
            for x in user_form.errors.as_data():
                messages.warning(request, user_form.errors[x][0])


    return render(request, 'sporcu/sporcu-ekle.html',
                  {'user_form': user_form, 'person_form': person_form, 'license_form':license_form, 'communication_form': communication_form

                   })

@login_required
def return_athletes(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    user_form = UserSearchForm()
    # # arama açıldıgı zaman burasi sillinecek
    # if user.groups.filter(name='KulupUye'):
    #     sc_user = SportClubUser.objects.get(user=user)
    #     clubsPk = []
    #     clubs = SportsClub.objects.filter(clubUser=sc_user)
    #     for club in clubs:
    #         clubsPk.append(club.pk)
    #     athletes = Athlete.objects.filter(licenses__sportsClub__in=clubsPk).distinct()
    # elif user.groups.filter(name__in=['Yonetim', 'Admin']):
    #     athletes = Athlete.objects.all()
    # #     silinecek son

    athletes = Athlete.objects.none()
    if request.method == 'POST':

        user_form = UserSearchForm(request.POST)
        brans=request.POST.get('branch')
        sportsclup=request.POST.get('sportsClub')



        if user_form.is_valid():
            firstName = user_form.cleaned_data.get('first_name')
            lastName = user_form.cleaned_data.get('last_name')
            email = user_form.cleaned_data.get('email')
            if  not (firstName or lastName or email or brans or sportsclup):

                if user.groups.filter(name='KulupUye'):
                    sc_user = SportClubUser.objects.get(user=user)
                    clubsPk = []
                    clubs = SportsClub.objects.filter(clubUser=sc_user)
                    for club in clubs:
                        clubsPk.append(club.pk)
                    athletes = Athlete.objects.filter(licenses__sportsClub__in=clubsPk).distinct()
                elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                    athletes = Athlete.objects.all()
            elif firstName or lastName or email or sportsclup or brans:
                query = Q()
                clubsPk = []
                clubs = SportsClub.objects.filter(name=request.POST.get('sportsClub'))
                for club in clubs:
                    clubsPk.append(club.pk)

                if firstName:
                    query &= Q(user__first_name__icontains=firstName)
                if lastName:
                    query &= Q(user__last_name__icontains=lastName)
                if email:
                    query &= Q(user__email__icontains=email)
                if sportsclup:
                    query &=Q(licenses__sportsClub__in=clubsPk)
                if brans:
                    query &= Q(licenses__branch=brans, licenses__status='Onaylandı')

                if user.groups.filter(name='KulupUye'):
                    sc_user = SportClubUser.objects.get(user=user)
                    clubsPk = []
                    clubs = SportsClub.objects.filter(clubUser=sc_user)
                    for club in clubs:
                        clubsPk.append(club.pk)
                    athletes = Athlete.objects.filter(licenses__sportsClub__in=clubsPk).filter(query).distinct()

                elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                    athletes = Athlete.objects.filter(query).distinct()

    sportclup = SearchClupForm(request.POST, request.FILES or None)
    if user.groups.filter(name='KulupUye'):
        sc_user = SportClubUser.objects.get(user=user)
        clubs = SportsClub.objects.filter(clubUser=sc_user)
        clubsPk = []
        for club in clubs:
            clubsPk.append(club.pk)
        sportclup.fields['sportsClub'].queryset = SportsClub.objects.filter(id__in=clubsPk)
    elif user.groups.filter(name__in=['Yonetim', 'Admin']):
        sportclup.fields['sportsClub'].queryset = SportsClub.objects.all()
    return render(request, 'sporcu/sporcular.html', {'athletes': athletes, 'user_form': user_form,'Sportclup': sportclup})
@login_required
def updateathletes(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    athlete = Athlete.objects.get(pk=pk)
    belts_form = athlete.belts.all()
    licenses_form = athlete.licenses.all()
    user = User.objects.get(pk=athlete.user.pk)
    person = Person.objects.get(pk=athlete.person.pk)
    communication = Communication.objects.get(pk=athlete.communication.pk)
    user_form = UserForm(request.POST or None, instance=user)
    person_form = PersonForm(request.POST or None, instance=person)
    communication_form = CommunicationForm(request.POST or None, instance=communication)
    say=0
    say=athlete.licenses.all().filter(status='Onaylandı').count()


    if request.method == 'POST':

        if user_form.is_valid() and communication_form.is_valid() and person_form.is_valid():
            user = user_form.save(commit=False)
            print('user=', user.first_name)
            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name'].upper()
            user.last_name = user_form.cleaned_data['last_name'].upper()
            user.email = user_form.cleaned_data['email']
            user.save()
            person_form.save()
            communication_form.save()


            messages.success(request, 'Sporcu Başarıyla Güncellenmiştir.')
            return redirect('sbs:update-athletes', pk=pk)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'sporcu/sporcuDuzenle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'belts_form': belts_form, 'licenses_form': licenses_form,
                   'athlete': athlete,'say':say})


@login_required
def return_belt(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    category_item_form = CategoryItemForm();

    if request.method == 'POST':

        category_item_form = CategoryItemForm(request.POST)

        if category_item_form.is_valid():

            categoryItem = category_item_form.save(commit=False)
            categoryItem.forWhichClazz = "BELT"
            categoryItem.save()
            messages.success(request, 'Kuşak Başarıyla Kayıt Edilmiştir.')
            return redirect('sbs:kusak')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')
    categoryitem = CategoryItem.objects.filter(forWhichClazz="BELT")
    return render(request, 'sporcu/kusak.html',
                  {'category_item_form': category_item_form, 'categoryitem': categoryitem})


@login_required
def categoryItemDelete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = CategoryItem.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def categoryItemUpdate(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    categoryItem = CategoryItem.objects.get(id=pk)
    category_item_form = CategoryItemForm(request.POST or None, instance=categoryItem,
                                          initial={'parent': categoryItem.parent})
    if request.method == 'POST':
        if category_item_form.is_valid():
            category_item_form.save()
            messages.success(request, 'Başarıyla Güncellendi')
            return redirect('sbs:kusak')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'sporcu/kusakDuzenle.html',
                  {'category_item_form': category_item_form})


@login_required
def sporcu_kusak_ekle(request, pk):
    perm = general_methods.control_access(request)


    if not perm:
        logout(request)
        return redirect('accounts:login')
    athlete = Athlete.objects.get(pk=pk)
    belt_form = BeltForm(request.POST, request.FILES or None)
    belt_form.fields['definition'].queryset=None
    for item in athlete.licenses.filter(status="Onaylandı"):
        veri=CategoryItem.objects.filter(forWhichClazz='BELT',branch=item.branch)
        if belt_form.fields['definition'].queryset==None:
            belt_form.fields['definition'].queryset=CategoryItem.objects.filter(forWhichClazz='BELT',branch=item.branch)
        else:
            belt_form.fields['definition'].queryset|=CategoryItem.objects.filter(forWhichClazz='BELT',branch=item.branch)


    # branch = athlete.licenses.last().branch
    # last olayı düzelecek
    # belt_form.fields['definition'].queryset = CategoryItem.objects.filter(forWhichClazz='BELT',athlete.licenses.last().branch)


    if request.method == 'POST':

        belt_form = BeltForm(request.POST, request.FILES or None)



        if belt_form.is_valid():

            belt = Level(startDate=belt_form.cleaned_data['startDate'],
                         dekont=belt_form.cleaned_data['dekont'],
                         definition=belt_form.cleaned_data['definition'],
                         form=belt_form.cleaned_data['form'],
                         city=belt_form.cleaned_data['city'],)


            belt.levelType = EnumFields.LEVELTYPE.BELT
            # last deger kaldirildi yerine alt satiır eklendi
            belt.branch = belt.definition.branch

            belt.status = Level.WAITED
            belt.save()
            athlete.belts.add(belt)
            athlete.save()

            messages.success(request, 'Kuşak Başarıyla Eklenmiştir.')
            return redirect('sbs:update-athletes', pk=pk)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'sporcu/sporcu-kusak-ekle.html',
                  {'belt_form': belt_form,})





@login_required
def sporcu_kusak_sil(request, pk, athlete_pk):
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Level.objects.get(pk=pk)
            athlete = Athlete.objects.get(pk=athlete_pk)
            athlete.belts.remove(obj)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Level.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def sporcu_lisans_ekle(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    athlete = Athlete.objects.get(pk=pk)
    user = request.user

    license_form = LicenseForm(request.POST, request.FILES or None)

    if user.groups.filter(name='KulupUye'):
        sc_user = SportClubUser.objects.get(user=user)
        clubs = SportsClub.objects.filter(clubUser=sc_user)
        clubsPk = []
        for club in clubs:
            clubsPk.append(club.pk)
        license_form.fields['sportsClub'].queryset = SportsClub.objects.filter(id__in=clubsPk)

    elif user.groups.filter(name__in=['Yonetim', 'Admin']):
        license_form.fields['sportsClub'].queryset = SportsClub.objects.all()

    if request.method == 'POST':
        license_form = LicenseForm(request.POST, request.FILES or None)
        if license_form.is_valid():
            license = license_form.save()
            athlete.licenses.add(license)
            athlete.save()
            messages.success(request, 'Lisans Başarıyla Eklenmiştir.')
            return redirect('sbs:update-athletes', pk=pk)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'sporcu/sporcu-lisans-ekle.html',
                  {'license_form': license_form})


@login_required
def sporcu_lisans_onayla(request, license_pk, athlete_pk):

    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        athlete = Athlete.objects.get(pk=athlete_pk)
        license = License.objects.get(pk=license_pk)
        for item in athlete.licenses.all():
            if item.branch == license.branch:
                item.isActive = False
                item.save()
        license.status = License.APPROVED
        license.isActive = True
        license.save()
        messages.success(request, 'Lisans Onaylanmıştır')
    except:
        messages.warning(request, 'Yeniden deneyiniz.')


    return redirect('sbs:update-athletes', pk=athlete_pk)


@login_required
def sporcu_lisans_reddet(request, license_pk, athlete_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        license = License.objects.get(pk=license_pk)
        license.reddetwhy = request.POST.get('reddetwhy')
        license.status = License.DENIED
        license.save()



    messages.success(request, 'Lisans Reddedilmiştir')
    return redirect('sbs:update-athletes', pk=athlete_pk)


@login_required
def sporcu_lisans_listesi_onayla(request, license_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        license = License.objects.get(pk=license_pk)
        athlete = license.athlete_set.first()
        for item in athlete.licenses.all():
            if item.branch == license.branch:
                item.isActive = False
                item.save()
        license.status = Level.APPROVED
        license.isActive = True
        license.save()
        messages.success(request, 'Lisans Onaylanmıştır')
    except:
        messages.success(request, 'Yeniden deneyiniz')



    return redirect('sbs:lisans-listesi')
@login_required
def sporcu_lisans_listesi_onayla_mobil(request, license_pk,count):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        license = License.objects.get(pk=license_pk)
        athlete = license.athlete_set.first()
        for item in athlete.licenses.all():
            if item.branch == license.branch:
                item.isActive = False
                item.save()
        license.status = License.APPROVED
        license.isActive = True
        license.save()
        messages.success(request, 'Lisans Onaylanmıştır')
    except:
        messages.warning(request, 'Yeniden deneyiniz')


    return redirect('sbs:sporcu-lisans-duzenle-mobil',count)
@login_required

def sporcu_lisans_listesi_reddet(request, license_pk):
    perm = general_methods.control_access(request)


    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.method == 'POST':
        license = License.objects.get(pk=license_pk)
        license.status = License.DENIED
        license.reddetwhy=request.POST.get('reddetwhy')
        license.save()
        messages.success(request, 'Lisans Reddedilmiştir')
    else:

        license = License.objects.get(pk=license_pk)
        license.status = License.DENIED
        license.save()
        messages.success(request, 'Lisans Reddedilmiştir')



    return redirect('sbs:lisans-listesi')

@login_required

def sporcu_lisans_listesi_reddet_mobil(request, license_pk,count):

    perm = general_methods.control_access(request)


    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.method == 'POST':
        license = License.objects.get(pk=license_pk)
        license.status = License.DENIED
        license.reddetwhy=request.POST.get('text')
        license.save()
        messages.success(request, 'Lisans Reddedilmiştir')
    else:

        license = License.objects.get(pk=license_pk)
        license.status = License.DENIED
        license.save()
        messages.success(request, 'Lisans Reddedilmiştir')

    return redirect('sbs:sporcu-lisans-duzenle-mobil',count)
@login_required
def sporcu_kusak_listesi_onayla(request, belt_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        belt = Level.objects.get(pk=belt_pk)
        athlete = belt.athlete_set.first()
        for item in athlete.belts.all():
            if item.branch == belt.branch:
                item.isActive = False
                item.save()
        belt.status = Level.APPROVED
        belt.isActive = True
        belt.save()
        messages.success(request, 'Kuşak Onaylanmıştır')
    except:
        messages.success(request, 'Yeniden deneyiniz')


    return redirect('sbs:kusak-listesi')
@login_required
def sporcu_kusak_listesi_reddet(request, belt_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    belt = Level.objects.get(pk=belt_pk)
    belt.status = Level.DENIED
    belt.save()
    messages.success(request, 'Kuşak reddedilmistir')
    return redirect('sbs:kusak-listesi')

# bütün kuşaklari onayla
@login_required
def sporcu_kusak_listesi_hepsinionayla(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        belt = Level.objects.filter(status='Beklemede', levelType=EnumFields.LEVELTYPE.BELT)
        for bt in belt:
            athlete = bt.athlete_set.first()
            for item in athlete.belts.all():
                if item.branch == bt.branch:
                    item.isActive = False
                    item.save()
            bt.status = Level.APPROVED
            bt.isActive = True
            bt.save()

        messages.success(request, 'Kuşaklar basari  Onaylanmıştır')
    except:
        messages.warning(request, 'Yeniden deneyiniz.')


    return redirect('sbs:kusak-listesi')


@login_required
def sporcu_kusak_onayla(request, belt_pk, athlete_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        belt = Level.objects.get(pk=belt_pk)
        athlete = Athlete.objects.get(pk=athlete_pk)
        for item in athlete.belts.all():
            if item.branch == belt.branch:
                item.isActive = False
                item.save()
        belt.status = Level.APPROVED
        belt.isActive = True
        belt.save()

        messages.success(request, 'Kuşak Onaylanmıştır')
    except:
        messages.warning(request, 'Yeniden deneyiniz.')


    return redirect('sbs:update-athletes', pk=athlete_pk)


@login_required
def sporcu_kusak_reddet(request, belt_pk,athlete_pk):
    perm = general_methods.control_access(request)


    if not perm:
        logout(request)
        return redirect('accounts:login')
    belt = Level.objects.get(pk=belt_pk)
    belt.status = Level.DENIED
    belt.save()

    messages.success(request, 'Kuşak Reddedilmiştir')
    return redirect('sbs:update-athletes', pk=athlete_pk)



# bütün kuşaklari beklemeye aldik
@login_required
def sporcu_kusak_bekle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    belt = Level.objects.all()
    for bt in belt:
        bt.status = Level.WAITED
        bt.save()

    messages.success(request, 'Kuşaklar beklemeye alindi ')
    return redirect('sbs:kusak-listesi')




@login_required
def sporcu_kusak_duzenle(request, belt_pk, athlete_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    belt = Level.objects.get(pk=belt_pk)
    athlete=Athlete.objects.get(pk=athlete_pk)
    belt_form = BeltForm(request.POST or None, request.FILES or None, instance=belt ,initial={'definition': belt.definition})
  # calismaalani
    belt_form.fields['definition'].queryset=None
    for item in athlete.licenses.filter(status="Onaylandı"):
        if belt_form.fields['definition'].queryset==None:
            belt_form.fields['definition'].queryset=CategoryItem.objects.filter(forWhichClazz='BELT',branch=item.branch)
        else:
            belt_form.fields['definition'].queryset|=CategoryItem.objects.filter(forWhichClazz='BELT',branch=item.branch)
    if request.method == 'POST':
        if belt_form.is_valid():
            belt.branch = belt.definition.branch
            belt_form.save()

            messages.success(request, 'Kuşak Onaya Gönderilmiştir.')
            return redirect('sbs:update-athletes', pk=athlete_pk)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'sporcu/sporcu-kusak-duzenle.html',
                  {'belt_form': belt_form})

@login_required
def sporcu_lisans_duzenle(request, license_pk, athlete_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    license = License.objects.get(pk=license_pk)


    license_form = LicenseForm(request.POST or None, request.FILES or None, instance=license,
                               initial={'sportsClub': license.sportsClub})
    user = request.user
    if user.groups.filter(name='KulupUye'):
        sc_user = SportClubUser.objects.get(user=user)
        clubs = SportsClub.objects.filter(clubUser=sc_user)
        clubsPk = []
        for club in clubs:
            clubsPk.append(club.pk)
        license_form.fields['sportsClub'].queryset = SportsClub.objects.filter(id__in=clubsPk)

    elif user.groups.filter(name__in=['Yonetim', 'Admin']):
        license_form.fields['sportsClub'].queryset = SportsClub.objects.all()

    if request.method == 'POST':
        if license_form.is_valid():
            license_form.save()
            if license.status !='Onaylandı':
                license.status =License.WAITED
                license.save()
            messages.success(request, 'Lisans Başarıyla Güncellenmiştir.')
            return redirect('sbs:update-athletes', pk=athlete_pk)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'sporcu/sporcu-lisans-duzenle.html',
                  {'license_form': license_form, 'license': license})




@login_required
def sporcu_lisans_duzenle_mobil_ilet(request):

    cout='0'
    return redirect('sbs:sporcu-lisans-duzenle-mobil',count=cout)

@login_required
def sporcu_lisans_duzenle_mobil(request, count):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    if user.groups.filter(name__in=['Yonetim', 'Admin']):
        ileri = int(count) + 1
        geri = int(count) - 1

        if int(count)>=0 and int(count)<License.objects.count():
            licenses = License.objects.all().order_by('-pk')[int(count)]
            if int(count)==0:
                geri=0;
        else:
            licenses = License.objects.all().order_by('-pk')[0]
            messages.success(request,'Degerler bitti ')
            count='0'



    return render(request, 'sporcu/sporcu-lisans-mobil-onay.html',
                  {'ileri':ileri ,'geri':geri,'say':count,'license': licenses})

@login_required
def sporcu_lisans_sil(request, pk, athlete_pk):
    perm = general_methods.control_access_klup(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = License.objects.get(pk=pk)
            athlete = Athlete.objects.get(pk=athlete_pk)
            athlete.licenses.remove(obj)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Level.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def sporcu_kusak_listesi(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    belts = not License.objects.none()
    if request.method == 'POST':
        brans = request.POST.get('branch')
        sportsclup = request.POST.get('sportsClub')
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        email = request.POST.get('email')
        status = request.POST.get('status')
        if firstName or lastName or email or sportsclup or brans or status:
            query = Q()
            if firstName:
                query &= Q(athlete__user__first_name__icontains=firstName)
            if lastName:
                query &= Q(athlete__user__last_name__icontains=lastName)
            if email:
                query &= Q(athlete__user__email__icontains=email)
            if sportsclup:
                try:
                    query &= Q(athlete__licenses__sportsClub=SportsClub.objects.get(name=sportsclup).pk)
                except:
                    if user.groups.filter(name__in=['Yonetim', 'Admin']):
                        messages.warning(request,'Bu kulube bir başkan atamasi gerçeklesmemiştir. Bütün degerler gösterilecek')
            if brans:
                query &= Q(branch__icontains=brans)
            if status:
                query &= Q(status=status)
            if user.groups.filter(name='KulupUye'):
                clubuser = SportClubUser.objects.get(user=user)
                clubs = SportsClub.objects.filter(clubUser=clubuser)
                clubsPk = []
                for club in clubs:
                    clubsPk.append(club.pk)
                belts = Level.objects.filter(query).filter(athlete__licenses__sportsClub__in=clubsPk).filter(levelType=EnumFields.LEVELTYPE.BELT).distinct()
            elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                belts = Level.objects.filter(query).filter(levelType=EnumFields.LEVELTYPE.BELT).distinct()
        else:
            if user.groups.filter(name='KulupUye'):
                clubuser = SportClubUser.objects.get(user=user)
                clubs = SportsClub.objects.filter(clubUser=clubuser)
                clubsPk = []
                for club in clubs:
                    clubsPk.append(club.pk)
                belts = Level.objects.filter(athlete__licenses__sportsClub__in=clubsPk).distinct()
            elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                belts = Level.objects.filter(levelType=EnumFields.LEVELTYPE.BELT).distinct()

    sportclup = SearchClupForm(request.POST, request.FILES or None)
    if user.groups.filter(name='KulupUye'):
        sc_user = SportClubUser.objects.get(user=user)
        clubs = SportsClub.objects.filter(clubUser=sc_user)
        clubsPk = []
        for club in clubs:
            clubsPk.append(club.pk)
        sportclup.fields['sportsClub'].queryset = SportsClub.objects.filter(id__in=clubsPk)
    elif user.groups.filter(name__in=['Yonetim', 'Admin']):
        sportclup.fields['sportsClub'].queryset = SportsClub.objects.all()
    return render(request, 'sporcu/sporcu-kusak-listesi.html', {'belts': belts,'Sportclup':sportclup})


@login_required
def sporcu_lisans_listesi(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    user_form=UserForm(request.POST, request.FILES or None)

    # ilk açılıs alani
    # if user.groups.filter(name='KulupUye'):
    #     clubuser = SportClubUser.objects.get(user=user)
    #     clubs = SportsClub.objects.filter(clubUser=clubuser)
    #     clubsPk = []
    #     for club in clubs:
    #         clubsPk.append(club.pk)
    #     licenses = License.objects.filter(athlete__licenses__sportsClub__in=clubsPk).distinct()
    #     sc_user = SportClubUser.objects.get(user=user)
    #     clubs = SportsClub.objects.filter(clubUser=sc_user)
    #     clubsPk = []
    #     for club in clubs:
    #         clubsPk.append(club.pk)
    #     sportclup.fields['sportsClub'].queryset = SportsClub.objects.filter(id__in=clubsPk)
    # elif user.groups.filter(name__in=['Yonetim', 'Admin']):
    #     licenses = License.objects.all().distinct()
    #     sportclup.fields['sportsClub'].queryset = SportsClub.objects.all()

    # ilk açılıs son
    licenses= not License.objects.none()
    if request.method == 'POST':
            brans = request.POST.get('branch')
            sportsclup = request.POST.get('sportsClub')
            firstName=request.POST.get('first_name')
            lastName=request.POST.get('last_name')
            email=request.POST.get('email')
            status = request.POST.get('status')

            if firstName or lastName or email or sportsclup or brans or status:
                query = Q()
                if firstName:
                    query &= Q(athlete__user__first_name__icontains=firstName)
                if lastName:
                    query &= Q(athlete__user__last_name__icontains=lastName)
                if email:
                    query &= Q(athlete__user__email__icontains=email)
                if sportsclup:
                    query &= Q(sportsClub__name__icontains=sportsclup)
                if brans:
                    query &= Q(branch__icontains=brans)
                if status:
                    query &= Q(status=status)

                if user.groups.filter(name='KulupUye'):

                    sc_user = SportClubUser.objects.get(user=user)
                    clubsPk = []
                    clubs = SportsClub.objects.filter(clubUser=sc_user)
                    for club in clubs:
                        clubsPk.append(club.pk)
                    licenses = License.objects.filter(sportsClub_id__in=clubsPk).filter(query).distinct()
                elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                    licenses = License.objects.filter(query).distinct()
            else:
                if user.groups.filter(name='KulupUye'):

                    sc_user = SportClubUser.objects.get(user=user)
                    clubsPk = []
                    clubs = SportsClub.objects.filter(clubUser=sc_user)
                    for club in clubs:
                        clubsPk.append(club.pk)
                    licenses = License.objects.filter(sportsClub_id__in=clubsPk).distinct()
                elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                    licenses = License.objects.all().distinct()

    sportclup = SearchClupForm(request.POST, request.FILES or None)
    if user.groups.filter(name='KulupUye'):
        sc_user = SportClubUser.objects.get(user=user)
        clubs = SportsClub.objects.filter(clubUser=sc_user)
        clubsPk = []
        for club in clubs:
            clubsPk.append(club.pk)
        sportclup.fields['sportsClub'].queryset = SportsClub.objects.filter(id__in=clubsPk)
    elif user.groups.filter(name__in=['Yonetim', 'Admin']):
        sportclup.fields['sportsClub'].queryset = SportsClub.objects.all()
    return render(request, 'sporcu/sporcu-lisans-listesi.html', {'licenses': licenses,'user_form':user_form,'Sportclup':sportclup})


@login_required
def updateAthleteProfile(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user = User.objects.get(pk=pk)
    directory_user = Athlete.objects.get(user=user)
    person = Person.objects.get(pk=directory_user.person.pk)
    communication = Communication.objects.get(pk=directory_user.communication.pk)
    user_form = DisabledUserForm(request.POST or None, instance=user)
    person_form = DisabledPersonForm(request.POST or None, request.FILES or None, instance=person)
    communication_form = DisabledCommunicationForm(request.POST or None, instance=communication)
    password_form = SetPasswordForm(request.user, request.POST)

    if request.method == 'POST':


        if user_form.is_valid() and communication_form.is_valid() and person_form.is_valid() and password_form.is_valid():

            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name'].upper()
            user.last_name = user_form.cleaned_data['last_name'].upper()
            user.email = user_form.cleaned_data['email']
            user.set_password(password_form.cleaned_data['new_password1'])
            user.save()

            person_form.save()
            communication_form.save()
            password_form.save()

            messages.success(request, 'Sporcu Başarıyla Güncellenmiştir.')

            return redirect('sbs:sporcu-profil-guncelle')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz ')

    return render(request, 'sporcu/sporcu-profil-guncelle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'password_form': password_form})



# lisanslarda beklemede olanlarin hepsini  onayla

@login_required
def sporcu_lisans_listesi_hepsionay(request):
    try:
        licenses = License.objects.filter(status='Beklemede')
        for license in licenses:
            athlete = license.athlete_set.first()
            for item in athlete.licenses.all():
                if item.branch == license.branch:
                    item.isActive = False
                    item.save()
            license.status = Level.APPROVED
            license.isActive = True
            license.save()
    except:
        messages.warning(request, 'Yeniden deneyiniz')


    return redirect('sbs:lisans-listesi')
# lisanslarda beklemede olanlarin hepsini reddet
@login_required
def sporcu_lisans_listesi_hepsireddet(request):

    licenses = License.objects.filter(status='Beklemede')
    for license in licenses:
        license.status = License.DENIED
        license.save()
    return redirect('sbs:lisans-listesi')

# bütün lisanslari beklemeye al
@login_required
def sporcu_bekle(request):

    licenses = License.objects.all()
    for license in licenses:
        license.status = License.WAITED
        license.save()
    return redirect('sbs:lisans-listesi')



# kuşaklarin beklemede olanlarini reddet
@login_required
def sporcu_kusak_hepsinireddet(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    belt = Level.objects.filter(status='Beklemede',levelType=EnumFields.LEVELTYPE.BELT)
    for bt in belt:
        bt.status = Level.DENIED
        bt.save()


    messages.success(request, 'Kuşaklar başari  Reddedilmiştir')
    return redirect('sbs:kusak-listesi')
