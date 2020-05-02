import datetime
from _socket import gaierror

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from sbs.Forms import VisaForm
from sbs.Forms.CategoryItemForm import CategoryItemForm
from sbs.Forms.CommunicationForm import CommunicationForm
from sbs.Forms.DisabledCommunicationForm import DisabledCommunicationForm
from sbs.Forms.DisabledPersonForm import DisabledPersonForm
from sbs.Forms.DisabledUserForm import DisabledUserForm
from sbs.Forms.GradeForm import GradeForm
from sbs.Forms.UserForm import UserForm
from sbs.Forms.VisaForm import VisaForm
from sbs.Forms.PersonForm import PersonForm
from sbs.Forms.CoachSearchForm import CoachSearchForm
from sbs.Forms.SearchClupForm import SearchClupForm

from sbs.Forms.UserSearchForm import UserSearchForm
from sbs.Forms.CompetitionForm import CompetitionForm
from sbs.Forms.VisaSeminarForm import VisaSeminarForm
from sbs.models import Coach, Athlete, Person, Communication, SportClubUser, Level, SportsClub
from sbs.models.CategoryItem import CategoryItem
from sbs.models.VisaSeminar import VisaSeminar
from sbs.models.EnumFields import EnumFields
from sbs.services import general_methods
from datetime import date,datetime
from django.utils import timezone

# visaseminer ekle
@login_required
def visaSeminar_ekle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visaSeminar = VisaSeminarForm()
    if request.method == 'POST':
        visaSeminar = VisaSeminarForm(request.POST)
        if visaSeminar.is_valid():

            visa = visaSeminar.save()
            visa.forWhichClazz = 'COACH'
            visa.save()
            messages.success(request, 'Vize Semineri Başari  Kaydedilmiştir.')

            return redirect('sbs:visa-seminar')
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'antrenor/visaSeminar-ekle.html',
                  {'competition_form': visaSeminar})


# visaseminar liste
@login_required
def return_visaSeminar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    Seminar = VisaSeminar.objects.filter(forWhichClazz='COACH')

    return render(request, 'antrenor/VisaSeminar.html', {'competitions': Seminar})

@login_required
def visaSeminar_duzenle(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    seminar= VisaSeminar.objects.get(pk=pk)
    coach=seminar.coach.all()
    competition_form = VisaSeminarForm(request.POST or None, instance=seminar)
    if request.method == 'POST':
        if competition_form.is_valid():
            competition_form.save()
            messages.success(request, 'Vize Seminer Başarıyla Güncellenmiştir.')

            return redirect('sbs:visa-seminar')
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')


    return render(request, 'antrenor/VizeSeminar-Duzenle.html',
                  {'competition_form': competition_form, 'competition': seminar, 'athletes': coach})


@login_required
def visaSeminar_sil(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = VisaSeminar.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Competition.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})




@login_required
def return_add_coach(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = UserForm()
    person_form = PersonForm()
    communication_form = CommunicationForm()

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST, request.FILES)
        communication_form = CommunicationForm(request.POST)

        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid():
            user = User()
            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name'].upper()
            user.last_name = user_form.cleaned_data['last_name'].upper()
            user.email = user_form.cleaned_data['email']
            group = Group.objects.get(name='Antrenor')
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

            coach = Coach(user=user, person=person, communication=communication)

            coach.save()
            # antroner kaydından sonra mail gönderilmeyecek

            # subject, from_email, to = 'Halter - Antrenör Bilgi Sistemi Kullanıcı Giriş Bilgileri', 'no-reply@twf.gov.tr', user.email
            # text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            # html_content = '<p> <strong>Site adresi: </strong> <a href="http://sbs.twf.gov.tr:81/"></a>sbs.twf.gov.tr:81</p>'
            # html_content = html_content + '<p><strong>Kullanıcı Adı:  </strong>' + user.username + '</p>'
            # html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            messages.success(request, 'Antrenör Başarıyla Kayıt Edilmiştir.')

            return redirect('sbs:antrenorler')

        else:

            for x in user_form.errors.as_data():
                messages.warning(request, user_form.errors[x][0])

    return render(request, 'antrenor/antrenor-ekle.html',
                  {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form})


@login_required
def return_coachs(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    coachs = Coach.objects.none()
    user_form = CoachSearchForm()
    searchClupForm = SearchClupForm()

    if request.method == 'POST':
        user_form = CoachSearchForm(request.POST)
        searchClupForm = SearchClupForm(request.POST)
        branch = request.POST.get('branch')
        grade = request.POST.get('definition')
        visa = request.POST.get('visa')
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        email = request.POST.get('email')

        if not (firstName or lastName or email or branch or grade or visa):
            if user.groups.filter(name='KulupUye'):
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                coachs = Coach.objects.filter(sportsclub__in=clubsPk).distinct()
            elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                coachs = Coach.objects.all()
        else:
            query = Q()
            if lastName:
                query &= Q(user__last_name__icontains=lastName)
            if firstName:
                query &= Q(user__first_name__icontains=firstName)
            if email:
                query &= Q(user__email__icontains=email)
            if branch:
                query &= Q(grades__branch=branch, grades__status='Onaylandı')
            if grade:
                query &= Q(grades__definition__name=grade, grades__status='Onaylandı')
            if visa == 'VISA':
                query &= Q(visa__startDate__year=timezone.now().year, visa__status='Onaylandı')

            if user.groups.filter(name='KulupUye'):
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                coachs = Coach.objects.filter(query).filter(sportsclub__in=clubsPk).distinct()
            elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                coachs = Coach.objects.filter(query)
            if visa == 'NONE':
                coachs = coachs.exclude(visa__startDate__year=timezone.now().year, visa__status='Onaylandı')
    return render(request, 'antrenor/antrenorler.html',
                  {'coachs': coachs, 'user_form': user_form, 'branch': searchClupForm})




@login_required
def return_grade(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    category_item_form = CategoryItemForm()

    if request.method == 'POST':

        category_item_form = CategoryItemForm(request.POST)
        name=request.POST.get('name')
        if name  is not None:
            categoryItem = CategoryItem(name=name)
            categoryItem.forWhichClazz = "COACH_GRADE"
            categoryItem.isFirst = False
            categoryItem.save()
            return redirect('sbs:kademe')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')
    categoryitem = CategoryItem.objects.filter(forWhichClazz="COACH_GRADE")
    return render(request, 'antrenor/kademe.html',
                  {'category_item_form': category_item_form, 'categoryitem': categoryitem})


@login_required
def antrenor_kademe_ekle(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    coach = Coach.objects.get(pk=pk)
    grade_form = GradeForm()
    category_item_form = CategoryItemForm()
    if request.method == 'POST':
        grade_form = GradeForm(request.POST, request.FILES)
        category_item_form=CategoryItemForm(request.POST, request.FILES)



        if  grade_form.is_valid() and grade_form.cleaned_data['dekont'] is not None and request.POST.get('branch') is not None:
            grade = Level(definition=grade_form.cleaned_data['definition'],
                          startDate=grade_form.cleaned_data['startDate'],
                          dekont=grade_form.cleaned_data['dekont'],
                          branch=grade_form.cleaned_data['branch'])
            grade.levelType = EnumFields.LEVELTYPE.GRADE
            grade.status = Level.WAITED
            grade.save()
            coach.grades.add(grade)
            coach.save()
            messages.success(request, 'Kademe Başarıyla Eklenmiştir.')
            return redirect('sbs:update-coach', pk=pk)

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    grade_form.fields['definition'].queryset = CategoryItem.objects.filter(forWhichClazz='COACH_GRADE')
    return render(request, 'antrenor/antrenor-kademe-ekle.html',
                  {'grade_form': grade_form})


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
    category_item_form = CategoryItemForm(request.POST or None, instance=categoryItem)
    if request.method == 'POST':
        if request.POST.get('name') is not None:
            categoryItem.name=request.POST.get('name')
            categoryItem.save()
            messages.warning(request, 'Başarıyla Güncellendi')
            return redirect('sbs:kademe')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'antrenor/kademeDuzenle.html',
                  {'category_item_form': category_item_form})


@login_required
def deleteCoach(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Coach.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Coach.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def coachUpdate(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    coach = Coach.objects.get(pk=pk)

    grade_form = coach.grades.all()
    visa_form=coach.visa.all()
    user = User.objects.get(pk=coach.user.pk)
    person = Person.objects.get(pk=coach.person.pk)
    communication = Communication.objects.get(pk=coach.communication.pk)
    user_form = UserForm(request.POST or None, instance=user)
    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    communication_form = CommunicationForm(request.POST or None, instance=communication)
    if request.method == 'POST':
        user = User.objects.get(pk=coach.user.pk)
        user_form = UserForm(request.POST or None, instance=user)
        # person_form = PersonForm(request.POST,request.FILES, instance=person)
        communication_form = CommunicationForm(request.POST or None, instance=communication)
        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid():

            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name'].upper()
            user.last_name = user_form.cleaned_data['last_name'].upper()
            user.email = user_form.cleaned_data['email']

            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['email']
            user.save()
            person_form.save()
            communication_form.save()

            messages.success(request, 'Antrenör Başarıyla Güncellendi')
            return redirect('sbs:antrenorler')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'antrenor/antrenorDuzenle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'grades_form': grade_form, 'coach': coach.pk,'personCoach':person,'visa_form':visa_form})


@login_required
def updateCoachProfile(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user =request.user
    directory_user = Coach.objects.get(user=user)
    person = Person.objects.get(pk=directory_user.person.pk)
    communication = Communication.objects.get(pk=directory_user.communication.pk)
    user_form = DisabledUserForm(request.POST or None, instance=user)
    person_form = DisabledPersonForm(request.POST or None, instance=person)
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

            messages.success(request, 'Antrenör Başarıyla Güncellenmiştir.')

            return redirect('sbs:antrenor-profil-guncelle')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'antrenor/antrenor-profil-guncelle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'password_form': password_form})

@login_required
def kademe_delete(request,grade_pk,coach_pk):
    perm = general_methods.control_access(request)


    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:

            obj =Level.objects.get(pk=grade_pk)
            coach = Coach.objects.get(pk=coach_pk)
            coach.grades.remove(obj)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Level.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def vize_delete(request,grade_pk,coach_pk):
    perm = general_methods.control_access(request)


    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:

            obj = Level.objects.get(pk=grade_pk)
            coach = Coach.objects.get(pk=coach_pk)
            coach.visa.remove(obj)
            obj.delete()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Level.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})



@login_required
def kademe_onay(request,grade_pk,coach_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = Level.objects.get(pk=grade_pk)
    coach = Coach.objects.get(pk=coach_pk)
    try:
        for item in coach.grades.all():
            if item.branch == grade.branch:
                item.isActive = False
                item.save()
        grade.status = Level.APPROVED
        grade.isActive = True
        grade.save()
        messages.success(request, 'Kademe   Onaylanmıştır')
    except:
        messages.warning(request, 'Lütfen yeniden deneyiniz.')
    return redirect('sbs:update-coach', pk=coach_pk)
@login_required
def visa_onay(request,grade_pk,coach_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = Level.objects.get(pk=grade_pk)
    visa.status = Level.APPROVED
    visa.save()

    messages.success(request, 'Vize onaylanmıştır')
    return redirect('sbs:update-coach', pk=coach_pk)

@login_required
def kademe_reddet(request,grade_pk,coach_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = Level.objects.get(pk=grade_pk)
    grade.status =Level.DENIED
    grade.save()

    messages.success(request, 'Kademe Reddedilmistir.')
    return redirect('sbs:update-coach', pk=coach_pk)


@login_required
def vize_reddet(request,grade_pk,coach_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = Level.objects.get(pk=grade_pk)
    visa.status = Level.DENIED
    visa.save()

    messages.warning(request, 'Vize Reddedilmistir.')
    return redirect('sbs:update-coach', pk=coach_pk)



@login_required
def kademe_update(request,grade_pk,coach_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade =Level.objects.get(pk=grade_pk)
    coach=Coach.objects.get(pk=coach_pk)
    categoryItem = Level.objects.get(pk=grade_pk)
    grade_form = GradeForm(request.POST or None, request.FILES or None, instance=grade,initial={'definition': grade.definition})
    if request.method == 'POST':
        if grade_form.is_valid():
            grade_form.save()
            messages.success(request, 'Kademe Başarılı bir şekilde güncellenmiştir.')
            return redirect('sbs:update-coach', pk=coach_pk)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'antrenor/kademe-update.html',
                  {'grade_form': grade_form})




@login_required
def kademe_list(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    coa = []
    for item in CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'):
        coa.append(item.pk)
    grade = Level.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE).distinct()
    return render(request, 'antrenor/Kademe-Listesi.html',
                  {'belts': grade })




@login_required
def vize_list(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    coa = []
    for item in CategoryItem.objects.filter(forWhichClazz='VISA'):
        coa.append(item.pk)
    grade = Level.objects.filter(definition_id__in=coa, levelType=EnumFields.VISA).distinct()
    return render(request, 'antrenor/Vize-Listesi.html',
                  {'belts': grade })



@login_required
def kademe_onayla(request, grade_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = Level.objects.get(pk=grade_pk)
    coach = grade.CoachGrades.first()
    try:
        for item in coach.grades.all():
            if item.branch == grade.branch:
                item.isActive = False
                item.save()
        grade.status = Level.APPROVED
        grade.isActive = True
        grade.save()
        messages.success(request, 'Kademe   Onaylanmıştır')
    except:
        messages.warning(request, 'Lütfen yeniden deneyiniz.')



    return redirect('sbs:kademe-listesi')

@login_required
def kademe_reddet_liste(request, grade_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = Level.objects.get(pk=grade_pk)
    grade.status = Level.DENIED
    grade.save()
    messages.success(request, 'Kademe   Onaylanmıştır')
    return redirect('sbs:kademe-listesi')

@login_required
def vize_onayla_liste(request, grade_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = Level.objects.get(pk=grade_pk)
    visa.status = Level.APPROVED
    visa.save()
    messages.success(request, 'Vize Onaylanmıştır')
    return redirect('sbs:vize-listesi')
@login_required
def vize_reddet_liste(request, grade_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = Level.objects.get(pk=grade_pk)
    visa.status = Level.DENIED
    visa.save()
    messages.success(request, 'Vize reddedilmistir.')
    return redirect('sbs:vize-listesi')


@login_required
def kademe_reddet_hepsi(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    coa = []
    for item in CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'):
        coa.append(item.pk)
    Belt = Level.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE, status="Beklemede")
    for belt in Belt:
        belt.status = CoachLevel.DENIED
        belt.save()
    messages.success(request, 'Beklemede olan kademeler   Onaylanmıştır')
    return redirect('sbs:kademe-listesi')


@login_required
def kademe_onay_hepsi(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    coa = []
    for item in CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'):
        coa.append(item.pk)
    Belt = Level.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE, status="Beklemede")

    for grade in Belt:
        coach = grade.CoachGrades.first()
        try:
            for item in coach.grades.all():
                if item.branch == grade.branch:
                    item.isActive = False
                    item.save()
            grade.status = Level.APPROVED
            grade.isActive = True
            grade.save()
            messages.success(request, 'Beklemede olan Kademeler Onaylanmıştır')
        except:
            messages.warning(request, 'Lütfen yeniden deneyiniz.')

    return redirect('sbs:kademe-listesi')


@login_required
def kademe_bekle_hepsi(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    Belt = CoachLevel.objects.filter(levelType=EnumFields.LEVELTYPE.GRADE)
    for belt in Belt:
        belt.status = CoachLevel.WAITED
        belt.save()
    messages.success(request, 'Kademe   Onaylanmıştır')
    return redirect('sbs:kademe-listesi')



@login_required
def antrenor_vısa_ekle(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    coach = Coach.objects.get(pk=pk)
    visa_form = VisaForm()
    category_item_form = CategoryItemForm()



    if request.method == 'POST':
        visa_form = VisaForm(request.POST, request.FILES)
        category_item_form=CategoryItemForm(request.POST, request.FILES)

        try:
            visa = Level(dekont=request.POST.get('dekont'), branch=request.POST.get('branch'))
            visa.startDate = date(int(request.POST.get('startDate')), 1, 1)
            visa.definition=CategoryItem.objects.get(forWhichClazz='VISA')
            visa.levelType = EnumFields.LEVELTYPE.VISA
            visa.status = Level.APPROVED

            for item in coach.visa.all():
                if item.branch == visa.branch:
                    item.isActive = False
                    item.save()
            visa.isActive = True
            visa.save()
            coach.visa.add(visa)
            coach.save()

            messages.success(request, 'Vize Başarıyla Eklenmiştir.')
            return redirect('sbs:update-coach', pk=pk)
        except:
            messages.warning(request, 'Alanları Kontrol Ediniz')


    return render(request, 'antrenor/Vize-ekle.html', {'grade_form': visa_form, 'category_item_form':category_item_form})

@login_required
def vize_update(request,grade_pk,coach_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade =Level.objects.get(pk=grade_pk)
    coach=Coach.objects.get(pk=coach_pk)
    grade_form = VisaForm(request.POST or None, request.FILES or None, instance=grade)

    if request.method == 'POST':
        if grade_form.is_valid():
            grade.save()
            messages.success(request, 'Vize Başarılı bir şekilde güncellenmiştir.')
            return redirect('sbs:update-coach', pk=coach_pk)
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')
    return render(request, 'antrenor/Vize-update.html',
                  {'grade_form': grade_form})


@login_required
def choose_coach(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    visa = VisaSeminar.objects.get(pk=pk)
    coa = []
    for item in visa.coach.all():
        coa.append(item.user.pk)

    athletes = Coach.objects.exclude(visaseminar__coach__user_id__in=coa)
    if request.method == 'POST':
        athletes1 = request.POST.getlist('selected_options')
        if athletes1:
            for x in athletes1:
                if not visa.coach.all().filter(beltexam__coachs__user_id=x):
                    visa.coach.add(x)
                    visa.save()
        return redirect('sbs:seminar-duzenle', pk=pk)
    return render(request, 'antrenor/visaSeminarCoach.html', {'athletes': athletes})


@login_required
def visaSeminar_Delete_Coach(request, pk, competition):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            visa = VisaSeminar.objects.get(pk=competition)
            visa.coach.remove(Coach.objects.get(pk=pk))
            visa.save()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def visaSeminar_onayla(request, pk):
    seminar = VisaSeminar.objects.get(pk=pk)
    if seminar.status == VisaSeminar.WAITED:
        visa = Level(dekont='Federasyon', branch=seminar.branch)
        visa.startDate = date(timezone.now().year, 1, 1)
        visa.definition = CategoryItem.objects.get(forWhichClazz='VISA')
        visa.levelType = EnumFields.LEVELTYPE.VISA
        visa.status = Level.APPROVED
        visa.save()

        for item in seminar.coach.all():

            for coach in item.visa.all():
                if coach.branch == visa.branch:
                    coach.isActive = False
                    coach.save()
            item.visa.add(visa)
            item.isActive = True
            item.save()
        seminar.status = VisaSeminar.APPROVED
        seminar.save()
    else:
        messages.warning(request, 'Seminer Daha Önce Onaylanmistir.')

    return redirect('sbs:seminar-duzenle', pk=pk)

    return render(request, 'antrenor/VisaSeminar.html')
    # {'grade_form': grade_form})
