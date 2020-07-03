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






@login_required
def return_technical_dashboard(request):
    perm = general_methods.control_access_technical(request)
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

    if not perm:
        logout(request)
        return redirect('accounts:login')
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
                                                      'lojman': lojman})



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
            return redirect('sbs:personel-profil-guncelle')

        else:
            return redirect('sbs:personel-profil-guncelle')

    return render(request, 'personel/Personel-Profil-güncelle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'password_form': password_form})
