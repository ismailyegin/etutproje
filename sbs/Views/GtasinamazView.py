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
from sbs.models.GTapu import
from sbs.models.Gteskilat import Gteskilat
from sbs.models.GkiraBedeli import GkiraBedeli

from sbs.Forms import GtasinmazForm


# from twisted.conch.insults.insults import privateModes


@login_required
def add_tasinmaz(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    item = Gtasinmaz.objects.all()

    project_form = GtasinmazForm()

    # if request.method == 'POST':
    #     project_form = EPProjectForm(request.POST)
    #
    #     project = project_form.save()
    #     project.town = request.POST.get('town')
    #     project.save()
    #
    #     log = str(project.name) + " projesini kaydetti"
    #     log = general_methods.logwrite(request, log)
    #
    #     messages.success(request, 'Proje Kaydedilmiştir.')
    #
    #     return redirect('sbs:proje-duzenle', pk=project.pk)

    return render(request, 'epproje/proje-ekle.html',
                  {'project_form': project_form})
