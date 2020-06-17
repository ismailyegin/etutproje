import re
from builtins import print
from datetime import datetime
from itertools import count

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from oxiterp.settings.base import MEDIA_URL
from sbs.Forms.CategoryItemForm import CategoryItemForm
from sbs.Forms.EPProjectForm import EPProjectForm
from sbs.models import EPProject, CategoryItem, City
from sbs.models.Town import Town
from sbs.models.Employee import Employee
from sbs.models.EPPhase import EPPhase
from sbs.services import general_methods
from sbs.services.general_methods import getProfileImage
from django.utils import timezone

from sbs.models.EPDocument import EPDocument
from sbs.Forms.EPDocumentForm import EPDocumentForm
from sbs.Forms.DisableEPProjectForm import DisableEPProjectForm


from sbs.Forms.EPProjectSearchForm import EPProjectSearchForm
from django.db.models import Q


@login_required
def add_project(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    project_form = EPProjectForm()

    if request.method == 'POST':
        project_form = EPProjectForm(request.POST)

        project = project_form.save()
        project.town = request.POST.get('town')
        project.save()

        messages.success(request, 'Proje Kaydedilmiştir.')

        return redirect('sbs:proje-duzenle', pk=project.pk)






        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.town=request.POST.get('town')
            project.save()

            messages.success(request, 'Proje Kaydedilmiştir.')

            return redirect('sbs:proje-duzenle', pk=project.pk)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'epproje/proje-ekle.html',
                  {'project_form': project_form})

@login_required
def edit_project_personel(request, pk):
    perm = general_methods.control_access_personel(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    user=request.user
    project = EPProject.objects.get(pk=pk)


    if project.sorumlu.user==user:
        print('Sorumlu')
        return redirect('sbs:proje-duzenle', pk=project.pk)


    else:
        project.town = Town.objects.get(pk=project.pk).name
        project_form = DisableEPProjectForm(request.POST or None, instance=project)
        days = None
        if project.aifinish:
            days = (project.aifinish - timezone.now()).days
            if days < 0:
                days = 'Alim işinin zamani bitti.'

        return render(request, 'epproje/Proje-incele-Personel.html',
                      {'project': project, 'project_form': project_form,
                       'days': days})







@login_required
def edit_project(request, pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    document_form=EPDocumentForm()
    project = EPProject.objects.get(pk=pk)
    user=request.user


    # güvenlik icin sorgu yapıldı

    try:

        if project.sorumlu.user != user:
            perm = general_methods.control_access(request)
            if not perm:
                logout(request)
                messages.warning(request, 'Bu alana girmeye yetkiniz yok.')
                return redirect('accounts:login')
    except:
        print('hata')
    project_form = EPProjectForm(request.POST or None, instance=project)
    titles = CategoryItem.objects.filter(forWhichClazz="EPPROJECT_EMPLOYEE_TITLE")
    employees = Employee.objects.all()
    days=None
    if project.aifinish:
        days= (project.aifinish-timezone.now()).days
        if days<0:
            days='Alim işinin zamani bitti.'

    if request.method == 'POST':
        try:
            document = request.FILES['files']
            data=EPDocument()
            data.name=document
            data.save()
            if document:
                project.documents.add(data)
                project.save()
        except:
            print('hata var')
        insaatAlani = request.POST.get('insaat')
        insaatAlani = insaatAlani.replace(".", "")
        insaatAlani = insaatAlani.replace(",", ".")

        tahmini = request.POST.get('tahmini')
        tahmini = tahmini.replace(".", "")
        tahmini = tahmini.replace(",", ".")

        yaklasik = request.POST.get('yaklasik')
        yaklasik = yaklasik.replace(".", "")
        yaklasik = yaklasik.replace(",", ".")

        sozlesmebedeli = request.POST.get('sozlesmebedeli')
        sozlesmebedeli = yaklasik.replace(".", "")
        sozlesmebedeli = yaklasik.replace(",", ".")

        sozlesmebedeliKdv = request.POST.get('sozlesmebedeliKdv')
        sozlesmebedeliKdv = yaklasik.replace(".", "")
        sozlesmebedeliKdv = yaklasik.replace(",", ".")

        arsa = request.POST.get('arsa')
        arsa = arsa.replace(".", "")
        arsa = arsa.replace(",", ".")

        town=request.POST.get('town')

        if project_form.is_valid():

            project = project_form.save(commit=False)
            project.insaatAlani = insaatAlani
            project.tahminiOdenekTutari = tahmini
            project.yaklasikMaliyet = yaklasik
            project.sozlesmeBedeli = sozlesmebedeli
            project.arsaAlani = arsa
            project.sozlesmeBedeliKdv=sozlesmebedeliKdv
            project.town=town


            project.save()

            messages.success(request, 'Proje Başarıyla Güncellendi')
            return redirect('sbs:proje-duzenle', pk=project.pk)
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'epproje/proje-duzenle.html',
                  {'project_form': project_form, 'project': project, 'titles': titles, 'employees': employees,'days':days})


@login_required
def return_projects(request):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    search_form=EPProjectSearchForm()
    projects=EPProject.objects.none()
    user = request.user
    projects = EPProject.objects.none()

    if request.method == 'POST':
        user_form = EPProjectSearchForm(request.POST)


        if user_form.is_valid() :
            name = user_form.cleaned_data.get('name')
            butceYili = user_form.cleaned_data.get('butceYili')
            butceCinsi = user_form.cleaned_data.get('butceCinsi')
            projeCinsi=user_form.cleaned_data.get('projeCinsi')
            city=user_form.cleaned_data.get('city')
            projectStatus=user_form.cleaned_data.get('projectStatus')

            if not (name or butceCinsi or butceYili or projeCinsi or projectStatus or city):

                if user.groups.filter(name='Personel'):
                    projects = EPProject.objects.filter(employees__employee__user=user).distinct()


                elif user.groups.filter(name__in=['Yonetim', 'Admin']):
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
                if projectStatus:
                    query &= Q(projectStatus=projectStatus)

                if user.groups.filter(name='Personel'):
                    projects = EPProject.objects.filter(query).filter(employees__employee__user=user).distinct()


                elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                    projects = EPProject.objects.filter(query).distinct()

    return render(request, 'epproje/projeler.html', {'projects': projects,'search_form':search_form})


@login_required
def return_projects_city(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    city = City.objects.get(pk=pk)
    projects = EPProject.objects.filter(city=city)
    search_form=EPProjectSearchForm()


    return render(request, 'epproje/projeler.html', {'projects': projects, 'city': city,'search_form':search_form})


@login_required
def return_employeetitles(request):
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
            categoryItem.forWhichClazz = "EPPROJECT_EMPLOYEE_TITLE"
            categoryItem.isFirst = False
            categoryItem.save()
            return redirect('sbs:unvanlar')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')
    categoryitem = CategoryItem.objects.filter(forWhichClazz="EPPROJECT_EMPLOYEE_TITLE")
    return render(request, 'epproje/unvanlar.html',
                  {'category_item_form': category_item_form, 'categoryitem': categoryitem})


@login_required
def delete_employeetitle(request, pk):
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
def edit_employeetitle(request, pk):
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
            return redirect('sbs:unvanlar')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'epproje/unvan-duzenle.html',
                  {'category_item_form': category_item_form})

@login_required
def update_employee_to_project(request, pk):
    perm = general_methods.control_access_personel(request)
    print('ben geldim ')



    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        project = EPProject.objects.get(pk=pk)
        id = request.POST.get('id')
        employees = project.employees.get(pk=id)

        if request.POST.get('title'):
            title = CategoryItem.objects.get(pk=request.POST.get('title'))
            employees.projectEmployeeTitle
        if request.POST.get('employee'):
            employee = Employee.objects.get(pk=request.POST.get('employee'))
            employees.employee = employee
        employees.save()
        project.save()



        return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
        messages.warning(request, 'Yeniden deneyiniz.')

    return redirect('sbs:proje-duzenle', pk=pk)


@login_required
def add_employee_to_project(request, pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        title = CategoryItem.objects.get(pk=request.POST.get('title'))
        employee = Employee.objects.get(pk=request.POST.get('employee'))
        project = EPProject.objects.get(pk=pk)
        employees=project.employees.create(projectEmployeeTitle=title, employee=employee)
        project.save()
        # messages.success(request, 'Personel Eklenmiştir')
        return JsonResponse({'status': 'Success', 'messages': 'save successfully','pk':employees.pk})

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
        messages.warning(request, 'Yeniden deneyiniz.')

    return redirect('sbs:proje-duzenle', pk=pk)


@login_required
def delete_employee_from_project(request, project_pk, employee_pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            athlete = EPProject.objects.get(pk=project_pk)
            athlete.employees.remove(employee_pk)
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except EPProject.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def update_requirement_to_project(request, pk):
    perm = general_methods.control_access_personel(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        amount = request.POST.get('amount')
        definition = request.POST.get('definition')
        id = request.POST.get('id')
        project = EPProject.objects.get(pk=pk)
        requirements=project.requirements.get(pk=id)
        requirements.amount=amount
        requirements.definition=definition
        requirements.save()
        project.save()

        # messages.success(request, 'İhtiyaç Eklenmiştir')
        return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
    except:
        messages.warning(request, 'Yeniden deneyiniz.')

    return redirect('sbs:proje-duzenle', pk=pk)




@login_required
def add_requirement_to_project(request, pk):
    perm = general_methods.control_access_personel(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        amount = request.POST.get('amount')
        definition = request.POST.get('definition')
        project = EPProject.objects.get(pk=pk)
        requirements=project.requirements.create(amount=amount, definition=definition)
        # messages.success(request, 'İhtiyaç Eklenmiştir')
        return JsonResponse({'status': 'Success', 'messages': 'save successfully','pk':requirements.pk})
    except:
        messages.warning(request, 'Yeniden deneyiniz.')

    return redirect('sbs:proje-duzenle', pk=pk)


@login_required
def delete_requirement_from_project(request, project_pk, employee_pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            athlete = EPProject.objects.get(pk=project_pk)
            athlete.requirements.remove(employee_pk)
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except EPProject.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def update_phase_to_project(request, pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')


    try:
        date = request.POST.get('phaseDate')
        dates = datetime.strptime(date, '%m/%d/%Y')
        definition = request.POST.get('phaseDefinition')
        id = request.POST.get('id')
        project = EPProject.objects.get(pk=pk)
        asama=project.phases.get(pk=id)
        asama.definition = definition
        asama.phaseDate = dates
        asama.save()
        project.save()
        return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
        messages.warning(request, 'Yeniden deneyiniz.')

    return redirect('sbs:proje-duzenle', pk=pk)




@login_required
def add_phase_to_project(request, pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')


    try:
        date = request.POST.get('phaseDate')
        dates = datetime.strptime(date, '%m/%d/%Y')
        definition = request.POST.get('phaseDefinition')
        project = EPProject.objects.get(pk=pk)
        asama = EPPhase()
        asama.definition = definition
        asama.phaseDate = dates
        asama.save()
        project.phases.add(asama)
        messages.success(request, 'Aşama Eklenmiştir')
        return JsonResponse({'status': 'Success', 'messages': 'save successfully','pk':asama.pk})

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
        messages.warning(request, 'Yeniden deneyiniz.')

    return redirect('sbs:proje-duzenle', pk=pk)


@login_required
def delete_phase_from_project(request, project_pk, employee_pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            athlete = EPProject.objects.get(pk=project_pk)
            athlete.phases.remove(employee_pk)
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except EPProject.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def add_offer_to_project(request, pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        message = request.POST.get('message')
        project = EPProject.objects.get(pk=pk)
        username = request.user.first_name + " " + request.user.last_name
        person = getProfileImage(request)
        imageUrl = MEDIA_URL + "profile/logo.png"
        date = datetime.now()
        dates = date.strftime('%d/%m/%Y %H:%M')

        project.offers.create(message=message, added_by=request.user)
        return JsonResponse({'status': 'Success', 'username': username, 'image': imageUrl, 'dates': dates})
    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    return redirect('sbs:proje-duzenle', pk=pk)








@login_required
def personel_list(request):
    perm = general_methods.control_access_personel(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        if request.method == 'GET':
            datatables = request.GET
            project = EPProject.objects.get(pk=request.GET.get('cmd'))
            say = 1
            beka = []
            for item in project.employees.all():
                data = {
                    'pk':item.pk,
                    'count': say,
                    'title': item.projectEmployeeTitle.name,
                    'employee': item.employee.user.first_name + ' ' + item.employee.user.last_name,
                }
                beka.append(data)
                say += 1
            total=project.employees.count()
            response = {
                'data': beka,
                'recordsTotal': total,
                'recordsFiltered': total,
            }
            return JsonResponse(response)

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    return redirect('sbs:proje-duzenle', pk=pk)


@login_required
def ihtiyac_list(request):
    perm = general_methods.control_access_personel(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        if request.method == 'GET':
            datatables = request.GET
            project = EPProject.objects.get(pk=request.GET.get('cmd'))
            say = 1
            beka = []
            for item in project.requirements.all():
                data = {
                    'pk': item.pk,
                    'count': say,
                    'title': item.amount,
                    'employee': item.definition,
                }
                beka.append(data)
                say += 1
            total = project.requirements.count()
            response = {
                'data': beka,
                'recordsTotal': total,
                'recordsFiltered': total,
            }
            return JsonResponse(response)

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    return redirect('sbs:proje-duzenle', pk=pk)
@login_required
def asama_list(request):
    perm = general_methods.control_access_personel(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        if request.method == 'POST':
            datatables = request.GET
            project = EPProject.objects.get(pk=request.POST.get('cmd'))
            say = 1
            beka = []
            for item in project.phases.all():
                data = {
                    'pk': item.pk,
                    'say': say,
                    'title':  item.phaseDate.strftime('%d/%m/%Y'),
                    'employee': item.definition,
                }
                beka.append(data)
                say += 1
            return JsonResponse({
                'data': beka
            })


    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    return redirect('sbs:proje-duzenle', pk=pk)

@login_required
def town(request):
    perm = general_methods.control_access_personel(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')


    try:
        if request.method == 'POST':
            project = Town.objects.filter(cityId__name=request.POST.get('cmd'))
            beka = []
            for item in project:
                data = {
                    'pk': item.pk,
                    'name': item.name,
                }
                beka.append(data)
            return JsonResponse(
                {
                    'data': beka,
                    'msg': 'Valid is  request'
                })

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def deleteReferee(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = EPProject.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Judge.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})



@login_required
def delete_document_project(request, project_pk, employee_pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            athlete = EPProject.objects.get(pk=project_pk)
            athlete.documents.remove(employee_pk)
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except EPProject.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})



@login_required
def dokumanAdd(request):




    perm = general_methods.control_access_personel(request)
    print('ben geldim')

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        project=EPProject.objects.get(pk=request.POST.get('pk'))

        document = request.FILES['file']
        data = EPDocument()
        data.name = document
        data.save()
        if document:
            project.documents.add(data)
            project.save()

        try:

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except EPProject.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def return_personel_dashboard(request):
    perm = general_methods.control_access_personel(request)
    user=request.user
    proje=EPProject.objects.filter(employees__employee__user=user).distinct()
    proje_count=proje.count()
    proje_status_PT=proje.filter(projectStatus=EPProject.PT).count()
    proje_status_PDE=proje.filter(projectStatus=EPProject.PDE).count()
    sorumlu_count=proje.filter(sorumlu__user=user).count()
    if not perm:
        logout(request)
        return redirect('accounts:login')
    return render(request, 'anasayfa/personel.html',{'proje_count':proje_count,'proje_status_PT':proje_status_PT,'sorumlu_count':sorumlu_count,'proje_status_PDE':proje_status_PDE})