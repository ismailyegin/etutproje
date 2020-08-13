import datetime
from _socket import gaierror

from django.contrib.auth import logout, authenticate, update_session_auth_hash
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
from sbs.Forms.EmployeeForm import EmployeeForm
from sbs.Forms.GradeForm import GradeForm
from sbs.Forms.UserForm import UserForm
from sbs.Forms.VisaForm import VisaForm
from sbs.Forms.PersonForm import PersonForm
from sbs.Forms.CoachSearchForm import CoachSearchForm
from sbs.Forms.SearchClupForm import SearchClupForm
from sbs.Forms.EPProjectSearchForm import EPProjectSearchForm
from sbs.Forms.DisableProjectFormTeknik import DisableProjectFormTeknik


from sbs.Forms.UserSearchForm import UserSearchForm
from sbs.Forms.CompetitionForm import CompetitionForm
from sbs.Forms.VisaSeminarForm import VisaSeminarForm
from sbs.Forms.DisableEPProjectForm import DisableEPProjectForm
from sbs.models import Coach, Athlete, Person, Communication, SportClubUser, Level, SportsClub
from sbs.models.CategoryItem import CategoryItem
from sbs.models.VisaSeminar import VisaSeminar
from sbs.models.EnumFields import EnumFields
from sbs.models.EPProject import EPProject
from sbs.models.Country import Country
from sbs.services import general_methods
from datetime import date, datetime
from django.utils import timezone
from sbs.models.Employee import Employee
from django.db.models import Sum





@login_required
def return_technical_dashboard(request):
    perm = general_methods.control_access_technical(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')



    user = request.user
    proje = EPProject.objects.all()

    proje_count = proje.count()
    proje_status_PT = proje.filter(projectStatus=EPProject.PT).count()
    proje_status_PDE = proje.filter(projectStatus=EPProject.PDE).count()
    sorumlu_count = Employee.objects.all().count()

    cezainfaz = proje.filter(projeCinsi=EPProject.CIK).count()
    adaletbinasi = proje.filter(projeCinsi=EPProject.AB).count()
    adlitip = proje.filter(projeCinsi=EPProject.AT).count()
    bolgeadliye = proje.filter(projeCinsi=EPProject.BAM).count()
    bolgeidari = proje.filter(projeCinsi=EPProject.BIM).count()
    denetimserbeslik = proje.filter(projeCinsi=EPProject.DS).count()
    personelegitim = proje.filter(projeCinsi=EPProject.PEM).count()
    bakanlikbinasi = proje.filter(projeCinsi=EPProject.BB).count()
    diger = proje.filter(projeCinsi=EPProject.DIGER).count()
    lojman = proje.filter(projeCinsi=EPProject.LOJMAN).count()

    projects = EPProject.objects.all().distinct()

    cezainfaz_sum = int(
        projects.filter(projeCinsi=EPProject.CIK).distinct().aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    adaletbinasi_sum = int(
        projects.filter(projeCinsi=EPProject.AB).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    adlitip_sum = int(projects.filter(projeCinsi=EPProject.AT).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    bolgeadliye_sum = int(
        projects.filter(projeCinsi=EPProject.BAM).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    bolgeidari_sum = int(
        projects.filter(projeCinsi=EPProject.BIM).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    denetimserbeslik_sum = int(
        projects.filter(projeCinsi=EPProject.DS).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    personelegitim_sum = int(
        projects.filter(projeCinsi=EPProject.PEM).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    bakanlikbinasi_sum = int(
        projects.filter(projeCinsi=EPProject.BB).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    diger_sum = int(projects.filter(projeCinsi=EPProject.DIGER).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    lojman_sum = int(
        projects.filter(projeCinsi=EPProject.LOJMAN).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)

    cezainfaz_tam = int(
        projects.filter(projeCinsi=EPProject.CIK, projectStatus=EPProject.PT).distinct().aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    adaletbinasi_tam = int(
        projects.filter(projeCinsi=EPProject.AB, projectStatus=EPProject.PT).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    adlitip_tam = int(
        projects.filter(projeCinsi=EPProject.AT, projectStatus=EPProject.PT).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    bolgeadliye_tam = int(
        projects.filter(projeCinsi=EPProject.BAM, projectStatus=EPProject.PT).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    bolgeidari_tam = int(
        projects.filter(projeCinsi=EPProject.BIM, projectStatus=EPProject.PT).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    denetimserbeslik_tam = int(
        projects.filter(projeCinsi=EPProject.DS, projectStatus=EPProject.PT).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    personelegitim_tam = int(
        projects.filter(projeCinsi=EPProject.PEM, projectStatus=EPProject.PT).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    bakanlikbinasi_tam = int(
        projects.filter(projeCinsi=EPProject.BB, projectStatus=EPProject.PT).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    diger_tam = int(
        projects.filter(projeCinsi=EPProject.DIGER, projectStatus=EPProject.PT).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    lojman_tam = int(
        projects.filter(projeCinsi=EPProject.LOJMAN, projectStatus=EPProject.PT).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)

    cezainfaz_dev = int(
        projects.filter(projeCinsi=EPProject.CIK, projectStatus=EPProject.PDE).distinct().aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    adaletbinasi_dev = int(
        projects.filter(projeCinsi=EPProject.AB, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    adlitip_dev = int(
        projects.filter(projeCinsi=EPProject.AT, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    bolgeadliye_dev = int(
        projects.filter(projeCinsi=EPProject.BAM, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    bolgeidari_dev = int(
        projects.filter(projeCinsi=EPProject.BIM, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    denetimserbeslik_dev = int(
        projects.filter(projeCinsi=EPProject.DS, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    personelegitim_dev = int(
        projects.filter(projeCinsi=EPProject.PEM, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    bakanlikbinasi_dev = int(
        projects.filter(projeCinsi=EPProject.BB, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    diger_dev = int(
        projects.filter(projeCinsi=EPProject.DIGER, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)
    lojman_dev = int(
        projects.filter(projeCinsi=EPProject.LOJMAN, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
            'insaatAlani__sum'] or 0)


    return render(request, 'anasayfa/Tehnical.html', {'proje_count': proje_count,
                                                      'proje_status_PT': proje_status_PT,
                                                      'sorumlu_count': sorumlu_count,
                                                      'proje_status_PDE': proje_status_PDE,
                                                      'proje_status_PT': proje_status_PT,
                                                      'proje_status_PDE': proje_status_PDE,
                                                      'cezainfaz': cezainfaz,
                                                      'adaletbinasi': adaletbinasi,
                                                      'adlitip': adlitip,
                                                      'bolgeadliye': bolgeadliye,
                                                      'bolgeidari': bolgeidari,
                                                      'denetimserbeslik': denetimserbeslik,
                                                      'personelegitim': personelegitim,
                                                      'bakanlikbinasi': bakanlikbinasi,
                                                      'diger': diger,
                                                      'lojman': lojman,

                                                      'cezainfaz_sum': cezainfaz_sum,
                                                      'adaletbinasi_sum': adaletbinasi_sum,
                                                      'adlitip_sum': adlitip_sum,
                                                      'bolgeadliye_sum': bolgeadliye_sum,
                                                      'bolgeidari_sum': bolgeidari_sum,
                                                      'denetimserbeslik_sum': denetimserbeslik_sum,
                                                      'personelegitim_sum': personelegitim_sum,
                                                      'bakanlikbinasi_sum': bakanlikbinasi_sum,
                                                      'diger_sum': diger_sum, 'lojman_sum': lojman_sum,

                                                      'cezainfaz_dev': cezainfaz_dev,
                                                      'adaletbinasi_dev': adaletbinasi_dev,
                                                      'adlitip_dev': adlitip_dev,
                                                      'bolgeadliye_dev': bolgeadliye_dev,
                                                      'bolgeidari_dev': bolgeidari_dev,
                                                      'denetimserbeslik_dev': denetimserbeslik_dev,
                                                      'personelegitim_dev': personelegitim_dev,
                                                      'bakanlikbinasi_dev': bakanlikbinasi_dev,
                                                      'diger_dev': diger_dev,
                                                      'lojman_dev': lojman_dev,

                                                      'cezainfaz_tam': cezainfaz_tam,
                                                      'adaletbinasi_tam': adaletbinasi_tam,
                                                      'adlitip_tam': adlitip_tam,
                                                      'bolgeadliye_tam': bolgeadliye_tam,
                                                      'bolgeidari_tam': bolgeidari_tam,
                                                      'denetimserbeslik_tam': denetimserbeslik_tam,
                                                      'personelegitim_tam': personelegitim_tam,
                                                      'bakanlikbinasi_tam': bakanlikbinasi_tam,
                                                      'diger_tam': diger_tam,
                                                      'lojman_tam': lojman_tam,

                                                      })



@login_required
def return_projects(request):
    perm = general_methods.control_access_technical(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    search_form = EPProjectSearchForm()
    projects = EPProject.objects.none()
    user = request.user

    if user.groups.filter(name__in=['Teknik', 'Admin']):
        get = request.GET.get('get')
        if get:
            if get == 'Projeler':
                projects = EPProject.objects.all()
            else:
                if get == 'TamamlananProje':
                    projects = EPProject.objects.filter(projectStatus=EPProject.PT)
                elif get == 'AçıkProje':
                    projects = EPProject.objects.filter(projectStatus=EPProject.PDE)

    elif user.groups.filter(name='Personel'):
        get = request.GET.get('get')
        if get:
            if get == 'Projeler':
                projects = EPProject.objects.filter(employees__employee__user=user).distinct()
                projects |= EPProject.objects.filter(sorumlu__user=user).distinct()
            elif get == 'TamamlananProje':
                projects = EPProject.objects.filter(projectStatus=EPProject.PT,
                                                    employees__employee__user=user).distinct()
                projects |= EPProject.objects.filter(projectStatus=EPProject.PT, sorumlu__user=user).distinct()
            elif get == 'AçıkProje':
                projects = EPProject.objects.filter(projectStatus=EPProject.PDE,
                                                    employees__employee__user=user).distinct()
                projects |= EPProject.objects.filter(projectStatus=EPProject.PDE, sorumlu__user=user).distinct()
            elif get == 'sorumlu':
                projects = EPProject.objects.filter(sorumlu__user=user).distinct()

    if request.method == 'POST':
        user_form = EPProjectSearchForm(request.POST)

        if user_form.is_valid():
            name = user_form.cleaned_data.get('name')
            butceYili = user_form.cleaned_data.get('butceYili')
            butceCinsi = user_form.cleaned_data.get('butceCinsi')
            projeCinsi = user_form.cleaned_data.get('projeCinsi')
            city = user_form.cleaned_data.get('city')
            Status = user_form.cleaned_data.get('projectStatus')

            if not (name or butceCinsi or butceYili or projeCinsi or Status or city):

                if user.groups.filter(name='Personel'):
                    projects = EPProject.objects.filter(employees__employee__user=user).distinct()
                    projects |= EPProject.objects.filter(sorumlu__user=user).distinct()


                elif user.groups.filter(name__in=['Teknik', 'Admin']):
                    projects = EPProject.objects.all()

            else:
                query = Q()
                if name:
                    query &= Q(name__icontains=name)
                if butceYili:
                    query &= Q(butceYili=butceYili)
                if butceCinsi:
                    query &= Q(butceCinsi=butceCinsi)
                if projeCinsi:
                    query &= Q(projeCinsi=projeCinsi)
                if city:
                    query &= Q(city=city)
                if Status:
                    query &= Q(projectStatus=Status)

                if user.groups.filter(name='Personel'):
                    projects = EPProject.objects.filter(query).filter(employees__employee__user=user).distinct()
                    projects |= EPProject.objects.filter(query).filter(sorumlu__user=user).distinct()

                elif user.groups.filter(name__in=['Teknik', 'Admin']):
                    projects = EPProject.objects.filter(query).distinct()

    return render(request, 'epproje/ProjelerTeknik.html', {'projects': projects, 'search_form': search_form})




@login_required
def edit_project_personel(request, pk):
    perm = general_methods.control_access_technical(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    project = EPProject.objects.get(pk=pk)
    projects = project.employees.all()
    print(project.city)


    project_form = DisableProjectFormTeknik(request.POST or None, instance=project)

    days = None
    if project.aifinish:
        days = (project.aifinish - timezone.now()).days


    return render(request, 'epproje/Proje-incele-teknik.html',
                  {'project': project, 'project_form': project_form,
                   'days': days})

@login_required
def updateRefereeProfile(request):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user = request.user
    referee_user = Employee.objects.get(user=user)
    person = Person.objects.get(pk=referee_user.person.pk)
    communication = Communication.objects.get(pk=referee_user.communication.pk)
    user_form = DisabledUserForm(request.POST or None, instance=user)
    person_form = DisabledPersonForm(request.POST or None, request.FILES or None, instance=person)
    communication_form = DisabledCommunicationForm(request.POST or None, instance=communication)
    password_form = SetPasswordForm(request.user, request.POST)

    if request.method == 'POST':
        person_form = DisabledPersonForm(request.POST, request.FILES)
        try:
            if request.FILES['profileImage']:
                print('deger var ')
                person.profileImage = request.FILES['profileImage']
                person.save()
                messages.success(request, 'Resim güncellendi.')

        except:
            print('hata' )


        if password_form.is_valid():
            user.set_password(password_form.cleaned_data['new_password2'])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifre Başarıyla Güncellenmiştir.')
            return redirect('sbs:teknik-profil-guncelle')

        else:
            return redirect('sbs:teknik-profil-guncelle')

    return render(request, 'personel/Personel-Profil-güncelle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'password_form': password_form})



@login_required
def return_employees(request):
    perm = general_methods.control_access(request)


    if not perm:
        logout(request)
        return redirect('accounts:login')

    user_form = UserSearchForm()
    employees = Employee.objects.none()



    if request.method == 'POST':
        user_form = UserSearchForm(request.POST)


        if user_form.is_valid() :
            firstName = user_form.cleaned_data.get('first_name')
            lastName = user_form.cleaned_data.get('last_name')
            email = user_form.cleaned_data.get('email')
            workDefinition=user_form.cleaned_data.get('workDefinition')
            if not (firstName or lastName or email or workDefinition):
                employees = Employee.objects.filter(user__groups__name="Teknik")
            else:
                query = Q()
                if lastName:
                    query &= Q(user__last_name__icontains=lastName)
                if firstName:
                    query &= Q(user__first_name__icontains=firstName)
                if email:
                    query &= Q(user__email__icontains=email)
                if workDefinition:
                    query &= Q(workDefinition=workDefinition)
                employees = Employee.objects.filter(query).filter(user__groups__name="Teknik").distinct()

    return render(request, 'personel/PersonellerTeknik.html',
                  {'employees': employees, 'user_form': user_form,})


@login_required
def add_employee(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = UserForm()
    person_form = PersonForm()

    communication=Communication()
    country=Country.objects.get(name='Türkiye')
    communication.country=country
    communication_form = CommunicationForm(instance=communication)

    employee_form = EmployeeForm()
    employee_form.fields['workDefinition'].queryset = CategoryItem.objects.filter(forWhichClazz="EMPLOYEE_WORKDEFINITION")

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST , request.FILES or None)
        communication_form = CommunicationForm(request.POST, request.FILES)

        sportClubUser_form = EmployeeForm(request.POST)

        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and sportClubUser_form.is_valid():
            user = User()
            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            group = Group.objects.get(name='Teknik')
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            user.groups.add(group)
            user.save()

            person = person_form.save(commit=False)
            communication = communication_form.save(commit=False)
            person.save()
            communication.save()

            personel = Employee(
                user=user, person=person, communication=communication,
                workDefinition=sportClubUser_form.cleaned_data['workDefinition'],

            )

            personel.save()

            messages.success(request, 'Personel Başarıyla Kayıt Edilmiştir.')

            return redirect('sbs:personeller-teknik')

        else:

            for x in user_form.errors.as_data():
                messages.warning(request, user_form.errors[x][0])

    return render(request, 'personel/personel-ekle.html',
                  {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form,
                   'employee_form': employee_form,
                   })