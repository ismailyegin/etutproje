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
from sbs.models import Athlete, CategoryItem, Person, Communication, License, SportClubUser, SportsClub, City, Country, \
    Coach, CompAthlete, Competition
from sbs.models.EnumFields import EnumFields
from sbs.models.Level import Level
from sbs.services import general_methods

from sbs.models.Logs import Logs

from accounts.models import Forgot

# page
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from sbs.models.simplecategory import simlecategory

@login_required
def return_log(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    logs = Logs.objects.none()
    user_form = UserSearchForm()
    if request.method == 'POST':
        user_form = UserSearchForm(request.POST)
        if user_form.is_valid():
            firstName = user_form.cleaned_data.get('first_name')
            lastName = user_form.cleaned_data.get('last_name')
            email = user_form.cleaned_data.get('email')

            if not (firstName or lastName or email):
                logs = Logs.objects.all().order_by('-creationDate')

            else:
                query = Q()
                if lastName:
                    query &= Q(user__last_name__icontains=lastName)
                if firstName:
                    query &= Q(user__first_name__icontains=firstName)
                if email:
                    query &= Q(user__email__icontains=email)

                logs = Logs.objects.filter(query).order_by('-creationDate')
    return render(request, 'Log/Logs.html', {'logs': logs, 'user_form': user_form})
