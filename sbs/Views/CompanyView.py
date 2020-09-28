from idlelib.idle_test.test_run import S
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

from sbs.Forms.CommunicationForm import CommunicationForm
from sbs.Forms.CompanyForm import CompanyForm
from sbs.models.Company import Company
from sbs.models.Communication import Communication

from sbs.services import general_methods
from datetime import date, datetime
import datetime
from django.utils import timezone
from django.contrib.auth.models import Group, Permission, User


@login_required
def return_add_Company(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    company_form = CompanyForm()
    communication_form = CommunicationForm()
    if request.method == 'POST':
        print('gelecek sensin ')
        company_form = CompanyForm(request.POST, request.FILES)
        communication_form = CommunicationForm(request.POST, request.FILES)
        if company_form.is_valid():

            communication = communication_form.save(commit=False)
            communication.save()
            company = company_form.save(commit=False)
            company.communication = communication
            company.save()

            messages.success(request, 'Şirket Kayıt Edilmiştir.')
            return redirect('sbs:company-list')
        else:
            print('alanlari kontrol ediniz')
            messages.warning(request, 'Alanları Kontrol Ediniz')
    return render(request, 'Company/Company.html',
                  {'company_form': company_form, 'communication_form': communication_form})


@login_required
def return_list_Company(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    company_form = Company.objects.all().order_by('-creationDate')
    print(company_form)
    for item in company_form:
        print(item.name)

    return render(request, 'Company/Companys.html',
                  {'company_form': company_form})


@login_required
def return_update_Company(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    company = Company.objects.get(pk=pk)
    company_form = CompanyForm(request.POST or None, instance=company)
    print(company_form)

    communication = Communication.objects.get(pk=company.communication.pk)
    communication_form = CommunicationForm(request.POST or None, instance=communication)

    if request.method == 'POST':
        if company_form.is_valid():
            communication = communication_form.save(commit=False)
            communication.save()
            company = company_form.save(commit=False)
            company.communication = communication
            company.save()

            messages.success(request, 'Şirket Güncellenmiştir.')
            return redirect('sbs:company-list')
        else:
            print('alanlari kontrol ediniz')
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'Company/CompanyUpdate.html',
                  {'company_form': company_form, 'communication_form': communication_form})