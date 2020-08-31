from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from sbs.Forms.CommunicationForm import CommunicationForm
from sbs.Forms.DisabledCommunicationForm import DisabledCommunicationForm
from sbs.Forms.DisabledPersonForm import DisabledPersonForm
from sbs.Forms.DisabledSportClubUserForm import DisabledSportClubUserForm
from sbs.Forms.DisabledUserForm import DisabledUserForm
from sbs.Forms.PersonForm import PersonForm
from sbs.Forms.SportClubUserForm import SportClubUserForm
from sbs.Forms.UserForm import UserForm
from sbs.Forms.UserSearchForm import UserSearchForm
from sbs.models import SportClubUser, Person, Communication
from sbs.services import general_methods


@login_required
def updateProfile(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user = request.user
    user_form = DisabledUserForm(request.POST or None, instance=user)
    password_form = SetPasswordForm(request.user, request.POST)

    if request.method == 'POST':

        if password_form.is_valid():

            user.set_password(password_form.cleaned_data['new_password1'])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifre Başarıyla Güncellenmiştir.')

            log = general_methods.logwrite(request, "admin sifre güncelledi")

            return redirect('sbs:admin-profil-guncelle')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'admin/admin-profil-guncelle.html',
                  {'user_form': user_form,'password_form':password_form})
