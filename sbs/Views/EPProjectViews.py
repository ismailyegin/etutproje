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
from sbs.Forms.CategoryItemForm import CategoryItemForm
from sbs.Forms.DisableEPProjectForm import DisableEPProjectForm
from sbs.Forms.EPDocumentForm import EPDocumentForm
from sbs.Forms.EPProjectForm import EPProjectForm
from sbs.Forms.EPProjectSearchForm import EPProjectSearchForm
from sbs.Forms.EPProjectSorumluForm import EPProjectSorumluForm
from sbs.models import EPProject, CategoryItem, City
from sbs.models.Company import Company
from sbs.models.EPDocument import EPDocument
from sbs.models.EPEmployee import EPEmployee
from sbs.models.EPPhase import EPPhase
from sbs.models.EPRequirements import EPRequirements
from sbs.models.EPVest import EPVest
from sbs.models.Employee import Employee
from sbs.models.Notification import Notification
from sbs.models.SubCompany import SubCompany
from sbs.models.Town import Town
from sbs.services import general_methods
from sbs.services.general_methods import getProfileImage
from sbs.models.EPNeedDocument import EPNeedDocument


# from twisted.conch.insults.insults import privateModes


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

        log = str(project.name) + " projesini kaydetti"
        log = general_methods.logwrite(request, log)

        messages.success(request, 'Proje Kaydedilmiştir.')

        return redirect('sbs:proje-duzenle', pk=project.pk)



    return render(request, 'epproje/proje-ekle.html',
                  {'project_form': project_form})


@login_required
def edit_project_personel(request, pk):
    perm = general_methods.control_access_personel(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    project = EPProject.objects.get(pk=pk)
    projects = project.employees.filter(employee__user=user)

    get = request.GET.get('notification')
    if get:
        notification = Notification.objects.get(pk=int(get))
        if notification.users == request.user:
            notification.is_show = True
            notification.save()

    if project.sorumlu:

        if project.sorumlu.user == user:
            return redirect('sbs:proje-duzenle', pk=project.pk)
        else:
            project_form = DisableEPProjectForm(request.POST or None, instance=project)
            days = None
            if project.aifinish:
                days = (project.aifinish - timezone.now()).days

            clubsPk = []
            for item in project.employees.filter(employee__user=user):
                clubsPk.append(int(item.projectEmployeeTitle.pk))
                print(item.projectEmployeeTitle.pk)
            titles = CategoryItem.objects.filter(id__in=clubsPk)
            test = []
            for item in titles:
                test.append(item.pk)
                print(item.name)
            subCompany = Company.objects.filter(JopDescription__id__in=test).distinct()

            for item in subCompany:
                print(item)
            return render(request, 'epproje/Proje-incele-Personel.html',
                          {'project': project, 'project_form': project_form,
                           'days': days, 'subCompany': subCompany, 'titles': titles})
    else:
        project_form = DisableEPProjectForm(request.POST or None, instance=project)
        days = None
        if project.aifinish:
            days = (project.aifinish - timezone.now()).days


        return render(request, 'epproje/Proje-incele-Personel.html',
                      {'project': project, 'project_form': project_form,
                       'days': days, 'employee': employee, 'company': company})






@login_required
def edit_project(request, pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    document_form = EPDocumentForm()
    project = EPProject.objects.get(pk=pk)
    user = request.user

    # for item in project.needDocument.all():
    #     print(item)

    # güvenlik icin sorgu yapıldı
    #
    # try:
    #     if project.sorumlu.user != user:
    #         perm = general_methods.control_access(request)
    #         if not perm:
    #             logout(request)
    #             messages.warning(request, 'Bu alana girmeye yetkiniz yok.')
    #             return redirect('accounts:login')
    # except:
    #     print('hata')



    if user.groups.filter(name='Personel'):
        project_form=EPProjectSorumluForm(request.POST or None, instance=project)



    elif user.groups.filter(name__in=['Yonetim', 'Admin']):
        project_form = EPProjectForm(request.POST or None, instance=project)

    else:
        project_form = EPProjectForm()
    company = Company.objects.all()
    titles = CategoryItem.objects.filter(forWhichClazz="EPPROJECT_EMPLOYEE_TITLE")
    employees = Employee.objects.all()

    days = None
    if project.aifinish:
        days = (project.aifinish - timezone.now()).days
        # if days < 0:
        #     days = 'Zamanı bitti.'


    get = request.GET.get('notification')
    if get:
        notification = Notification.objects.get(pk=int(get))
        if notification.users == request.user:
            notification.is_show = True
            notification.save()

    if request.method == 'POST':

        # document = request.FILES['needfiles']
        # data = EPNeedDocument()
        # data.name = document
        # data.save()
        # project.documents.add(data)
        # project.save()

        try:
            if request.FILES['needfiles']:
                document = request.FILES['needfiles']
                data = EPNeedDocument()
                data.name = document
                data.save()
                project.needDocument.add(data)
                project.save()
        except:
            print('neeed error')


        try:
            if request.FILES['files']:
                document = request.FILES['files']
                data = EPDocument()
                data.name = document
                data.save()
                project.documents.add(data)
                project.save()

        except:
            print('documnet none ')
        insaatAlani = request.POST.get('insaat')
        insaatAlani = insaatAlani.replace(".", "")
        insaatAlani = insaatAlani.replace(",", ".")

        tahmini = request.POST.get('tahmini')
        tahmini = tahmini.replace(".", "")
        tahmini = tahmini.replace(",", ".")

        # yaklasik = request.POST.get('yaklasik')
        # yaklasik = yaklasik.replace(".", "")
        # yaklasik = yaklasik.replace(",", ".")

        sozlesmebedeli = request.POST.get('sozlesmebedeli')
        sozlesmebedeli = sozlesmebedeli.replace(".", "")
        sozlesmebedeli = sozlesmebedeli.replace(",", ".")

        sozlesmebedeliKdv = request.POST.get('sozlesmebedeliKdv')
        sozlesmebedeliKdv = sozlesmebedeliKdv.replace(".", "")
        sozlesmebedeliKdv = sozlesmebedeliKdv.replace(",", ".")

        arsa = request.POST.get('arsa')
        arsa = arsa.replace(".", "")
        arsa = arsa.replace(",", ".")

        town = request.POST.get('town')

        if project.sorumlu:
            sorumlu = project.sorumlu

        if project_form.is_valid():
            projectSave = project_form.save(commit=False)
            projectSave.insaatAlani = insaatAlani
            projectSave.tahminiOdenekTutari = tahmini
            # projectSave.yaklasikMaliyet = yaklasik
            projectSave.sozlesmeBedeli = sozlesmebedeli
            projectSave.arsaAlani = arsa
            projectSave.sozlesmeBedeliKdv = sozlesmebedeliKdv
            projectSave.town = town
            projectSave.save()
            if request.POST.get('sorumlu'):
                if request.POST.get('sorumlu') is None and sorumlu:
                    projectSave.sorumlu = sorumlu
            projectSave.save()

            log = str(project.name) + "projesini güncelledi"
            log = general_methods.logwrite(request, log)

            messages.success(request, 'Proje Başarıyla Güncellendi')
            return redirect('sbs:proje-duzenle', pk=project.pk)
        else:

            print('Alanlari kontrol ediniz')
            messages.warning(request, 'Alanları Kontrol Ediniz')
    return render(request, 'epproje/proje-duzenle.html',
                  {'project_form': project_form,
                   'project': project,
                   'titles': titles,
                   'employees': employees,
                   'days': days,
                   'company': company})


@login_required
def return_detay(request):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    get = request.GET.get('get')

    cins = ''
    cins_sum = 0
    cins_tam = 0
    cins_dev = 0

    if user.groups.filter(name='Personel'):

        projects = EPProject.objects.filter(employees__employee__user=user).distinct()
        projects |= EPProject.objects.filter(sorumlu__user=user).distinct()


    elif user.groups.filter(name__in=['Teknik', 'Admin']):
        projects = EPProject.objects.all().distinct()
    else:
        projects = EPProject.objects.all().distinct()




    projects = EPProject.objects.all().distinct()

    cezainfaz = int(
        projects.filter(projeCinsi=EPProject.CIK).distinct().aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    adaletbinasi = int(
        projects.filter(projeCinsi=EPProject.AB).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    adlitip = int(projects.filter(projeCinsi=EPProject.AT).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    bolgeadliye = int(
        projects.filter(projeCinsi=EPProject.BAM).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    bolgeidari = int(
        projects.filter(projeCinsi=EPProject.BIM).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    denetimserbeslik = int(
        projects.filter(projeCinsi=EPProject.DS).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    personelegitim = int(
        projects.filter(projeCinsi=EPProject.PEM).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    bakanlikbinasi = int(
        projects.filter(projeCinsi=EPProject.BB).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    ATGV = int(projects.filter(projeCinsi=EPProject.ATGV).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)

    diger = int(projects.filter(projeCinsi=EPProject.DIGER).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)

    lojman = int(
        projects.filter(projeCinsi=EPProject.LOJMAN).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    if get:
        cins = get
        cins_sum = int(EPProject.objects.filter(projeCinsi=get).distinct().aggregate(Sum('insaatAlani'))[
                           'insaatAlani__sum'] or 0)
        cins_tam = int(EPProject.objects.filter(projeCinsi=cins, projectStatus=EPProject.PT).distinct().aggregate(
            Sum('insaatAlani'))['insaatAlani__sum'] or 0)
        cins_dev = int(EPProject.objects.filter(projeCinsi=cins, projectStatus=EPProject.PDE).distinct().aggregate(
            Sum('insaatAlani'))['insaatAlani__sum'] or 0)

    return render(request, 'epproje/detay-grafik.html',
                  {'isim': cins, 'cins_dev': cins_dev, 'cins_sum': cins_sum, 'cins_tam': cins_tam,
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
                   'ATGV': ATGV
                   })


def currency(dollars):
    dollars = round(float(dollars), 2)
    return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])

@login_required
def return_projects(request):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    search_form = EPProjectSearchForm(initial={'karakteristik': ''})
    projects = EPProject.objects.none()
    user = request.user

    if user.groups.filter(name__in=['Yonetim', 'Admin']):
        get = request.GET.get('get')
        if get:
            if get == 'Projeler':
                projects = EPProject.objects.all()
            elif get == 'TamamlananProje':
                projects = EPProject.objects.filter(projectStatus=EPProject.PT)
            elif get == 'AçıkProje':
                projects = EPProject.objects.filter(projectStatus=EPProject.PDE)
            elif get == 'durdurulanProje':
                projects = EPProject.objects.filter(projectStatus=EPProject.PD)
            elif get == 'iptalProje':
                projects = EPProject.objects.filter(projectStatus=EPProject.PIE)
            else:
                projects = EPProject.objects.filter(pk=int(get))

        employes = request.GET.get('employes')

        if employes:
            employe = Employee.objects.get(pk=int(employes))
            projects = EPProject.objects.filter(employees__employee__user=employe.user,
                                                projectStatus=EPProject.PDE).distinct()
            projects |= EPProject.objects.filter(sorumlu__user=employe.user, projectStatus=EPProject.PDE).distinct()
            # projects = EPProject.objects.filter(employees__employee=employe).distinct()





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
            karakteristik=user_form.cleaned_data.get('karakteristik')

            if not (name or butceCinsi or butceYili or projeCinsi or Status or city or karakteristik):

                if user.groups.filter(name='Personel'):
                    projects = EPProject.objects.filter(employees__employee__user=user).distinct()
                    projects |= EPProject.objects.filter(sorumlu__user=user).distinct()


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
                if Status:
                    query &= Q(projectStatus=Status)
                if karakteristik:
                    query &= Q(karakteristik=karakteristik)

                if user.groups.filter(name='Personel'):
                    projects = EPProject.objects.filter(query).filter(employees__employee__user=user).distinct()
                    projects |= EPProject.objects.filter(query).filter(sorumlu__user=user).distinct()

                elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                    projects = EPProject.objects.filter(query).distinct()

    return render(request, 'epproje/projeler.html', {'projects': projects, 'search_form': search_form})


@login_required
def return_projects_city(request, pk):
    perm = general_methods.control_access_personel(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    city = City.objects.get(pk=pk)
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)

    if user.groups.filter(name__in=['Teknik', 'Admin']):
        projects = EPProject.objects.filter(city=city)


    elif user.groups.filter(name='Personel'):
        projects = EPProject.objects.filter(employees__employee__user=user).distinct()
        projects |= EPProject.objects.filter(sorumlu__user=user).distinct()
        projects = projects.filter(city=city)

    return render(request, 'epproje/proje-il.html', {'projects': projects, 'city': city})


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
            return redirect('sbs:istanimiListesi')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')
    categoryitem = CategoryItem.objects.filter(forWhichClazz="EPPROJECT_EMPLOYEE_TITLE")
    return render(request, 'epproje/istanimlari.html',
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
def project_subfirma(request, pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    project = EPProject.objects.get(pk=pk)

    if request.POST.get('title') and request.POST.get('company'):
        title = CategoryItem.objects.get(pk=request.POST.get('title'))
        company = Company.objects.get(pk=request.POST.get('company'))
        subcompany = SubCompany(jopDescription=title, company=company)
        subcompany.save()
        project.subcompany.add(subcompany)
        project.save()

    try:
        print()
        return JsonResponse({'status': 'Success', 'messages': 'save successfully', 'pk': subcompany.pk})

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
        messages.warning(request, 'Yeniden deneyiniz.')

    return redirect('sbs:proje-duzenle', pk=pk)


@login_required
def update_employee_to_project(request, pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    project = EPProject.objects.get(pk=pk)
    id = request.POST.get('id')
    employees = project.employees.get(pk=id)

    if request.POST.get('title'):
        title = CategoryItem.objects.get(pk=request.POST.get('title'))
        employees.projectEmployeeTitle = title

        log = str(project.name) + " projesinde " + str(
            employees.employee.user.get_full_name()) + " personeli unvan  =" + str(title) + "olarak güncellendi "
        log = general_methods.logwrite(request, log)

    if request.POST.get('employee'):
        employee = Employee.objects.get(pk=request.POST.get('employee'))
        employees.employee = employee
        log = str(project.name) + " projesinde " + str(employee.user.get_full_name()) + " personeli personel =" + str(
            employee) + "olarak güncellendi "
        log = general_methods.logwrite(request, log)
    employees.save()
    project.save()

    try:
        print()
        return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
        messages.warning(request, 'Yeniden deneyiniz.')

    return redirect('sbs:proje-duzenle', pk=pk)

@login_required
def update_subcompany_to_project(request, pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    project = EPProject.objects.get(pk=pk)

    subcompany = project.subcompany.get(pk=request.POST.get('id'))

    if request.POST.get('title'):
        title = CategoryItem.objects.get(pk=request.POST.get('title'))
        subcompany.jopDescription = title
        subcompany.save()

    if request.POST.get('company'):
        company = Company.objects.get(pk=request.POST.get('company'))
        subcompany.company = company
        subcompany.save()
    log = str(project.name) + " projesinde  alt firma güncelledi"
    log = general_methods.logwrite(request, log)

    project.save()

    try:
        print()
        return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
        messages.warning(request, 'Yeniden deneyiniz.')

    return redirect('sbs:proje-duzenle', pk=pk)


@login_required
def update_subcompany_information_to_project(request, pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    project = EPProject.objects.get(pk=pk)
    subcompany = project.subcompany.get(pk=request.POST.get('id'))

    return JsonResponse({'status': 'Success',
                         'messages': 'save successfully',
                         'cName': subcompany.company.name,
                         'cMail': subcompany.company.mail,
                         'cUser': subcompany.company.sorumlu,
                         'cType': 'Bireysel' if subcompany.company.isFormal else 'Kurumsal',
                         'cCepTel': subcompany.company.communication.phoneNumber,
                         'cSabitTel': subcompany.company.communication.phoneNumber2,
                         })

    try:
        print()


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
        # personel kaydedildi
        title = CategoryItem.objects.get(pk=request.POST.get('title'))
        employee = Employee.objects.get(pk=request.POST.get('employee'))
        project = EPProject.objects.get(pk=pk)
        employees = project.employees.create(projectEmployeeTitle=title, employee=employee)
        project.save()
        # bildirimler gönderiliyor
        notification = Notification(
            users=employee.user,
            entityId=project.pk,
            tableName="proje"
        )
        notification.notification = project.name + ' projesine eklendiniz'
        notification.save()

        # işlemin log kaydı eklenedi

        log = str(project.name) + " projesine " + str(employee) + " ekledi unvan =" + str(title)
        log = general_methods.logwrite(request, log)

        # messages.success(request, 'Personel Eklenmiştir')
        return JsonResponse({'status': 'Success', 'messages': 'save successfully', 'pk': employees.pk})


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
            project = EPProject.objects.get(pk=project_pk)

            log = str(project.name) + " projesininden " + str(
                EPEmployee.objects.get(pk=employee_pk).employee.user.get_full_name()) + " personeli sildi"
            log = general_methods.logwrite(request, log)
            project.employees.remove(employee_pk)
            project.save()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except EPProject.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def delete_subcompany_project(request, project_pk, employee_pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            project = EPProject.objects.get(pk=project_pk)

            log = str(project.name) + " projesininden  alt firma silindi" + str(
                SubCompany.objects.get(pk=employee_pk))
            log = general_methods.logwrite(request, log)
            subcompany = SubCompany.objects.get(pk=employee_pk)
            project.subcompany.remove(subcompany)
            project.save()
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
        requirements = project.requirements.get(pk=id)
        requirements.amount = amount
        requirements.definition = definition
        requirements.save()
        project.save()

        log = str(project.name) + " projesinde ihtiyacı günceleledi adet=" + str(amount) + "Tanım =" + str(definition)
        log = general_methods.logwrite(request, log)




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
        requirements = project.requirements.create(amount=amount, definition=definition)

        log = str(project.name) + " projesine yeni ihtiyaç ekledi adet=" + str(amount) + "Tanım =" + str(definition)
        log = general_methods.logwrite(request, log)


        # messages.success(request, 'İhtiyaç Eklenmiştir')
        return JsonResponse({'status': 'Success', 'messages': 'save successfully', 'pk': requirements.pk})
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
            project = EPProject.objects.get(pk=project_pk)
            requirements = EPRequirements.objects.get(pk=employee_pk)

            log = str(project.name) + " projesinde ihtiyac silindi  adet=" + str(requirements.amount) + "Tanım =" + str(
                requirements.definition)
            log = general_methods.logwrite(request, log)


            project.requirements.remove(employee_pk)
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
        asama = project.phases.get(pk=id)
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
        dates = datetime.strptime(date, '%d/%m/%Y')
        definition = request.POST.get('phaseDefinition')
        project = EPProject.objects.get(pk=pk)

        for item in project.employees.all().distinct():
            notification = Notification(notification=project.name+" Projesine yeni bir aşama eklendi",
                                        users=item.employee.user,
                                        entityId=project.pk,
                                        tableName="proje"
                                        )
            notification.save()




        asama = EPPhase()
        asama.definition = definition
        asama.phaseDate = dates
        asama.save()
        project.phases.add(asama)

        log = str(project.name) + " projesine asama ekledi id=" + str(asama.pk)
        log = general_methods.logwrite(request, log)



        messages.success(request, 'Aşama Eklenmiştir')
        return JsonResponse({'status': 'Success', 'messages': 'save successfully', 'pk': asama.pk})

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
        messages.warning(request, 'Yeniden deneyiniz.')

    return redirect('sbs:proje-duzenle', pk=pk)

@login_required
def delete_ofters_from_project(request, project_pk, employee_pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            athlete = EPProject.objects.get(pk=project_pk)
            athlete.offers.remove(employee_pk)
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except EPProject.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

@login_required
def delete_phase_from_project(request, project_pk, employee_pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        try:
            project = EPProject.objects.get(pk=project_pk)

            asama = EPPhase.objects.get(pk=employee_pk)

            log = str(project.name) + " projesinde asama sildi id=" + str(asama.pk)
            log = general_methods.logwrite(request, log)
            project.phases.remove(employee_pk)

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

    message = request.POST.get('message')
    project = EPProject.objects.get(pk=pk)
    username = request.user.first_name + " " + request.user.last_name
    person = getProfileImage(request)
    imageUrl = MEDIA_URL + "profile/logo.png"
    date = datetime.now()
    dates = date.strftime('%d/%m/%Y %H:%M')

    log = str(project.name) + " projesine yeni bir görüs ekledi time=" + str(dates)
    log = general_methods.logwrite(request, log)

    project.offers.create(message=message, added_by=request.user)

    for item in project.employees.all().exclude(employee__user=request.user):
        notification = Notification(notification=project.name +" Projesine yeni bir görüs eklendi.",
                                    users=item.employee.user,
                                    entityId=project.pk,
                                    tableName="proje"
                                    )
        notification.save()





    try:
        print()





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
                    'pk': item.pk,
                    'count': say,
                    'title': item.projectEmployeeTitle.name,
                    'employee': item.employee.user.first_name + ' ' + item.employee.user.last_name,
                }
                beka.append(data)
                say += 1
            total = project.employees.count()
            response = {
                'data': beka,
                'recordsTotal': total,
                'recordsFiltered': total,
            }
            return JsonResponse(response)

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})




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
                    'title': item.phaseDate.strftime('%d/%m/%Y'),
                    'employee': item.definition,
                }
                beka.append(data)
                say += 1
            return JsonResponse({
                'data': beka
            })


    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})




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
        except :
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def delete_needdocument_project(request, project_pk, employee_pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            athlete = EPProject.objects.get(pk=project_pk)
            athlete.needDocument.remove(employee_pk)
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except EPProject.DoesNotExist:
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

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        project = EPProject.objects.get(pk=request.POST.get('pk'))

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
    user = request.user

    proje = EPProject.objects.filter(employees__employee__user=user).distinct()
    proje |= EPProject.objects.filter(sorumlu__user=user).distinct()

    proje_count = proje.count()
    proje_status_PT = proje.filter(projectStatus=EPProject.PT).count()
    proje_status_PDE = proje.filter(projectStatus=EPProject.PDE).count()
    sorumlu_count = EPProject.objects.filter(sorumlu__user=user).count()




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

    projects = proje

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












    if not perm:
        logout(request)
        return redirect('accounts:login')
    return render(request, 'anasayfa/personel.html', {'proje_count': proje_count,
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
def add_vest_to_project(request, pk):
    perm = general_methods.control_access_personel(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    vest = request.POST.get('vest')
    date = request.POST.get('vestdate')
    dates = datetime.strptime(date, '%d/%m/%Y')

    project = EPProject.objects.get(pk=pk)
    vest = project.vest.create(vest=vest, vestDate=dates)

    log = str(project.name) + " hakedis ekledi " + str(vest.vest)
    log = general_methods.logwrite(request, log)


    return JsonResponse({'status': 'Success', 'messages': 'save successfully', 'pk': vest.pk})


@login_required
def delete_vest_from_project(request, project_pk, employee_pk):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            project = EPProject.objects.get(pk=project_pk)

            vest = EPVest.objects.get(pk=employee_pk)
            log = str(project.name) + " hakedis sildi " + str(vest.vest)
            log = general_methods.logwrite(request, log)
            project.vest.remove(employee_pk)

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except EPProject.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def update_vest_to_project(request, pk):
    perm = general_methods.control_access_personel(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    vest = request.POST.get('vest')
    date = request.POST.get('vestdate')
    dates = datetime.strptime(date, '%d/%m/%Y')
    # print(type(vest))

    vestobject = EPVest.objects.get(pk=pk)
    vestobject.vest = Decimal(vest)
    vestobject.vestDate = dates
    vestobject.save()

    log = str(vestobject.pk) + "     hakedis güncellendi."
    log = general_methods.logwrite(request, log)



    return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

    try:
        print('')



    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
        messages.warning(request, 'Yeniden deneyiniz.')

    return redirect('sbs:proje-duzenle', pk=pk)


@login_required
def return_projects_mimar(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    get = request.GET.get('employe')
    if get:
        employe = Employee.objects.filter(workDefinition__name=get)
    else:
        employe = Employee.objects.filter(workDefinition__name="MİMAR")

    data = []
    for item in employe:
        print(item.user)
        eprojects = EPProject.objects.filter(projectStatus=EPProject.PDE,
                                             employees__employee__user=item.user).distinct()
        etotalsum = int(eprojects.aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
        ecezainfaz_dev = int(
            eprojects.filter(projeCinsi=EPProject.CIK, projectStatus=EPProject.PDE).distinct().aggregate(
                Sum('insaatAlani'))[
                'insaatAlani__sum'] or 0)
        eadaletbinasi_dev = int(
            eprojects.filter(projeCinsi=EPProject.AB, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
                'insaatAlani__sum'] or 0)
        eadlitip_dev = int(
            eprojects.filter(projeCinsi=EPProject.AT, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
                'insaatAlani__sum'] or 0)
        ebolgeadliye_dev = int(
            eprojects.filter(projeCinsi=EPProject.BAM, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
                'insaatAlani__sum'] or 0)
        ebolgeidari_dev = int(
            eprojects.filter(projeCinsi=EPProject.BIM, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
                'insaatAlani__sum'] or 0)
        edenetimserbeslik_dev = int(
            eprojects.filter(projeCinsi=EPProject.DS, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
                'insaatAlani__sum'] or 0)
        epersonelegitim_dev = int(
            eprojects.filter(projeCinsi=EPProject.PEM, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
                'insaatAlani__sum'] or 0)
        ebakanlikbinasi_dev = int(
            eprojects.filter(projeCinsi=EPProject.BB, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
                'insaatAlani__sum'] or 0)
        ediger_dev = int(
            eprojects.filter(projeCinsi=EPProject.DIGER, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
                'insaatAlani__sum'] or 0)
        elojman_dev = int(
            eprojects.filter(projeCinsi=EPProject.LOJMAN, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
                'insaatAlani__sum'] or 0)
        eatvg_dev = int(
            eprojects.filter(projeCinsi=EPProject.ATGV, projectStatus=EPProject.PDE).aggregate(Sum('insaatAlani'))[
                'insaatAlani__sum'] or 0)

        beka = {
            'count': eprojects.count(),
            'employe': item,
            'totalsum': etotalsum,
            'eatvg_dev': eatvg_dev,
            'elojman_dev': elojman_dev,
            'ediger_dev': ediger_dev,
            'ebakanlikbinasi_dev': ebakanlikbinasi_dev,
            'ebakanlikbinasi_dev': ebakanlikbinasi_dev,
            'epersonelegitim_dev': epersonelegitim_dev,
            'edenetimserbeslik_dev': edenetimserbeslik_dev,
            'ebolgeidari_dev': ebolgeidari_dev,
            'ebolgeadliye_dev': ebolgeadliye_dev,
            'eadlitip_dev': eadlitip_dev,
            'eadaletbinasi_dev': eadaletbinasi_dev,
            'ecezainfaz_dev': ecezainfaz_dev,

        }
        data.append(beka)

    return render(request, 'epproje/Mimarlar.html',
                  {'data': data})
