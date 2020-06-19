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


from sbs.Forms.UserSearchForm import UserSearchForm
from sbs.Forms.CompetitionForm import CompetitionForm
from sbs.Forms.VisaSeminarForm import VisaSeminarForm
from sbs.models import Coach, Athlete, Person, Communication, SportClubUser, Level, SportsClub
from sbs.models.CategoryItem import CategoryItem
from sbs.models.Employee import Employee
from sbs.models.VisaSeminar import VisaSeminar
from sbs.models.EnumFields import EnumFields
from sbs.models.EPProject import EPProject
from sbs.models.Country import Country
from sbs.services import general_methods
from datetime import date, datetime
from django.utils import timezone


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
            group = Group.objects.get(name='Personel')
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

            return redirect('sbs:personeller')

        else:

            for x in user_form.errors.as_data():
                messages.warning(request, user_form.errors[x][0])

    return render(request, 'personel/personel-ekle.html',
                  {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form,
                   'employee_form': employee_form,
                   })











@login_required
def edit_employee(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    employee = Employee.objects.get(pk=pk)
    user = User.objects.get(pk=employee.user.pk)
    person = Person.objects.get(pk=employee.person.pk)

    communication = Communication.objects.get(pk=employee.communication.pk)
    user_form = UserForm(request.POST or None, instance=user)
    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    communication_form = CommunicationForm(request.POST or None, instance=communication)

    employee_form = EmployeeForm(request.POST or None, instance=employee)
    employee_form.fields['workDefinition'].queryset = CategoryItem.objects.filter(
        forWhichClazz="EMPLOYEE_WORKDEFINITION")
    projects=EPProject.objects.filter(employees__employee__user=user ).distinct()
    projects|=EPProject.objects.filter(sorumlu__user=user).distinct()

    if request.method == 'POST':

        if user_form.is_valid() and communication_form.is_valid() and person_form.is_valid() and employee_form.is_valid():

            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.save()
            person_form.save()
            communication_form.save()
            employee_form.save()

            messages.success(request, 'Personel Başarıyla Güncellenmiştir.')

            # return redirect('sbs:personeller')

        else:

            for x in user_form.errors.as_data():
                messages.warning(request, user_form.errors[x][0])

    return render(request, 'personel/personel-duzenle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'employee_form': employee_form,'projects':projects,'personel':user})

@login_required
def delete_employee(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Employee.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Coach.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


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
                employees = Employee.objects.all()
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
                employees = Employee.objects.filter(query).distinct()

    return render(request, 'personel/personeller.html',
                  {'employees': employees, 'user_form': user_form,})


@login_required
def return_workdefinitions(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    category_item_form = CategoryItemForm()

    if request.method == 'POST':

        category_item_form = CategoryItemForm(request.POST)
        name = request.POST.get('name')
        if name is not None:
            categoryItem = CategoryItem(name=name)
            categoryItem.forWhichClazz = "EMPLOYEE_WORKDEFINITION"
            categoryItem.isFirst = False
            categoryItem.save()
            return redirect('sbs:istanimlari')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')
    categoryitem = CategoryItem.objects.filter(forWhichClazz="EMPLOYEE_WORKDEFINITION")
    return render(request, 'personel/istanimlari.html',
                  {'category_item_form': category_item_form, 'categoryitem': categoryitem})



@login_required
def delete_workdefinition(request, pk):
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
def edit_workdefinition(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    categoryItem = CategoryItem.objects.get(id=pk)
    category_item_form = CategoryItemForm(request.POST or None, instance=categoryItem)
    if request.method == 'POST':
        if request.POST.get('name') is not None:
            categoryItem.name = request.POST.get('name')
            categoryItem.save()
            messages.success(request, 'Başarıyla Güncellendi')
            return redirect('sbs:istanimlari')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'personel/istanimi-duzenle.html',
                  {'category_item_form': category_item_form})



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





