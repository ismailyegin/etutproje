from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from sbs.Forms.EPProjectForm import EPProjectForm
from sbs.models import EPProject
from sbs.services import general_methods


@login_required
def add_project(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    project_form = EPProjectForm()

    if request.method == 'POST':
        project_form = EPProjectForm(request.POST)
        if project_form.is_valid():
            project_form.save()
            messages.success(request, 'Proje Kaydedilmiştir.')

            return redirect('sbs:projeler')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'epproje/proje-ekle.html',
                  {'project_form': project_form})


@login_required
def edit_project(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    project = EPProject.objects.get(pk=pk)
    project_form = EPProjectForm(request.POST or None, instance=project)
    if request.method == 'POST':
        if project_form.is_valid() :

            project_form.save()

            messages.success(request, 'Proje Başarıyla Güncellendi')
            return redirect('sbs:projeler')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'epproje/proje-duzenle.html',
                  {'project_form': project_form})


@login_required
def return_projects(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    projects = EPProject.objects.all()

    return render(request, 'epproje/projeler.html', {'projects': projects})
