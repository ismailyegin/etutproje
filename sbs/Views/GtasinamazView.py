from builtins import print
from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from rest_framework.fields import empty

from oxiterp.settings.base import MEDIA_URL

from sbs.models.Town import Town
from sbs.services import general_methods

from sbs.models.Gtasinmaz import Gtasinmaz
from sbs.models.Gkira import Gkira
from sbs.models.Gtahsis import Gtahsis
from sbs.models.Gkurum import Gkurum
from sbs.models.GTapu import GTapu
from sbs.models.Gteskilat import Gteskilat
from sbs.models.GkiraBedeli import GkiraBedeli

from sbs.Forms.GtasinmazForm import GtasinmazForm


# from twisted.conch.insults.insults import privateModes


@login_required
def add_tasinmaz(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    project_form = GtasinmazForm()

    if request.method == 'POST':
        project_form = GtasinmazForm(request.POST)
        if project_form.is_valid():
            project = project_form.save()
            log = str(project.name) + " tasınmaz  kaydetti"
            log = general_methods.logwrite(request, log)

            messages.success(request, 'Tasınmaz  Kaydedilmiştir.')

            return redirect('sbs:tasinmaz-duzenle', pk=project.pk)
        else:
            messages.warning(request, 'Alanları kontrol ediniz.')
    return render(request, 'tasinmaz/tasinmazEkle.html',
                  {'project_form': project_form})


@login_required
def edit_tasinmaz(request, pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    project = Gtasinmaz.objects.get(pk=pk)
    user = request.user

    project_form = GtasinmazForm(request.POST or None, instance=project)

    if request.method == 'POST':

        project_form = GtasinmazForm(request.POST)
        if project_form.is_valid():
            projectSave = project_form.save()
            log = str(project.name) + "tasinmaz  güncelledi"
            log = general_methods.logwrite(request, log)

            messages.success(request, 'Tasinmaz Başarıyla Güncellendi')
            return redirect('sbs:tasinmaz-duzenle', pk=project.pk)
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')
    return render(request, 'tasinmaz/tasinmazGuncelle.html',
                  {'project_form': project_form,
                   'project': project, })
