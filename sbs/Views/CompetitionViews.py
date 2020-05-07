from itertools import combinations

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from sbs.Forms.CompetitionForm import CompetitionForm
from sbs.Forms.CompetitionSearchForm import CompetitionSearchForm
from django.db.models import Q
from sbs.models import SportClubUser, SportsClub, Competition, Athlete, CompAthlete, Weight
from sbs.models.SimpleCategory import SimpleCategory
from sbs.models.EnumFields import EnumFields
from sbs.models.SandaAthlete import SandaAthlete
from sbs.models.TaoluAthlete import TaoluAthlete
from sbs.services import general_methods
from sbs.Forms.SimplecategoryForm import SimplecategoryForm

from datetime import date,datetime
from django.utils import timezone


@login_required
def categori_ekle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    simplecategoryForm = SimplecategoryForm()
    categoryitem = SimpleCategory.objects.all()
    if request.method == 'POST':
        simplecategoryForm = SimplecategoryForm(request.POST)
        if simplecategoryForm.is_valid():
            simplecategoryForm.save()
            messages.success(request, 'Kategori Başarıyla Güncellenmiştir.')
        else:
            messages.warning(request, 'Birşeyler ters gitti yeniden deneyiniz.')

    return render(request, 'musabaka/müsabaka-Simplecategori.html',
                  {'category_item_form': simplecategoryForm, 'categoryitem': categoryitem})


@login_required
def return_competitions(request):

    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    comquery=CompetitionSearchForm()
    competitions = Competition.objects.filter(registerStartDate__lte=timezone.now(),registerFinishDate__gte=timezone.now())

    if request.method == 'POST':
        name= request.POST.get('name')
        startDate= request.POST.get('startDate')
        compType= request.POST.get('compType')
        compGeneralType= request.POST.get('compGeneralType')
        if name or startDate or compType or compGeneralType:
            query = Q()
            if name:
                query &= Q(name__icontains=name)
            if startDate:
                query &= Q(startDate__year=int(startDate))
            if compType:
                query &= Q(compType__in=compType)
            if compGeneralType:
                query &= Q(compGeneralType__in=compGeneralType)
            competitions=Competition.objects.filter(query).distinct()
        else:
            competitions = Competition.objects.all()
    return render(request, 'musabaka/musabakalar.html', {'competitions': competitions,'query':comquery})


@login_required
def musabaka_ekle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    competition_form = CompetitionForm()
    if request.method == 'POST':
        competition_form = CompetitionForm(request.POST)
        if competition_form.is_valid():
            competition_form.save()
            messages.success(request, 'Müsabaka Başarıyla Kaydedilmiştir.')

            return redirect('sbs:musabakalar')
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'musabaka/musabaka-ekle.html',
                  {'competition_form': competition_form})


@login_required
def musabaka_duzenle(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    musabaka = Competition.objects.get(pk=pk)
    athletes = CompAthlete.objects.filter(competition=pk)
    competition_form = CompetitionForm(request.POST or None, instance=musabaka)
    if request.method == 'POST':
        if competition_form.is_valid():
            competition_form.save()
            messages.success(request, 'Müsabaka Başarıyla Güncellenmiştir.')

            return redirect('sbs:musabaka-duzenle', pk=pk)
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'musabaka/musabaka-duzenle.html',
                  {'competition_form': competition_form, 'competition': musabaka, 'athletes': athletes})


@login_required
def musabaka_sil(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Competition.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Competition.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def musabaka_sporcu_ekle(request, athlete_pk, competition_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.method == 'POST':
        compAthlete = CompAthlete()
        compAthlete.athlete = Athlete.objects.get(pk=athlete_pk)
        compAthlete.competition = Competition.objects.get(pk=competition_pk)
        compAthlete.sıklet = Weight.objects.get(pk=request.POST.get('weight'))
        compAthlete.total = request.POST.get('total')
        compAthlete.save()
        messages.success(request, 'Sporcu Eklenmiştir')

    return redirect('sbs:lisans-listesi')


@login_required
def musabaka_sporcu_sec(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    print(pk)
    weights = Weight.objects.all()
    # login_user = request.user
    # user = User.objects.get(pk=login_user.pk)
    # competition = Competition.objects.get(pk=pk)
    # weights = Weight.objects.all()
    # if user.groups.filter(name='KulupUye'):
    #     sc_user = SportClubUser.objects.get(user=user)
    #     clubsPk = []
    #     clubs = SportsClub.objects.filter(clubUser=sc_user)
    #     for club in clubs:
    #         clubsPk.append(club.pk)
    #     athletes = Athlete.objects.filter(licenses__sportsClub__in=clubsPk).distinct()
    # elif user.groups.filter(name__in=['Yonetim', 'Admin']):
    #     athletes = Athlete.objects.all()

    return render(request, 'musabaka/musabaka-sporcu-sec.html',
                  {'pk':pk,'weights': weights})
                  # ,{'athletes': athletes, 'competition': competition, })

@login_required
def return_sporcu(request):
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    # /datatablesten gelen veri kümesi datatables degiskenine alindi
    if request.method == 'GET':
        datatables = request.GET
        pk = request.GET.get('cmd')
        # print('pk beklenen deger =',pk)
        competition = Competition.objects.get(pk=pk)
        # kategori = CompetitionCategori.objects.get(pk=request.GET.get('cmd'))

    elif request.method == 'POST':
        datatables = request.POST
        # print(datatables)
        # print("post islemi gerceklesti")

    # /Sayfanın baska bir yerden istenmesi durumunda degerlerin None dönmemesi icin degerler try boklari icerisine alindi
    try:
        draw = int(datatables.get('draw'))
        # print("draw degeri =", draw)
        # Ambil start
        start = int(datatables.get('start'))
        # print("start degeri =", start)
        # Ambil length (limit)
        length = int(datatables.get('length'))
        # print("lenght  degeri =", length)
        # Ambil data search
        search = datatables.get('search[value]')
        # print("search degeri =", search)
    except:
        draw = 1
        start = 0
        length = 10

    if length == -1:
        if user.groups.filter(name='KulupUye'):
            sc_user = SportClubUser.objects.get(user=user)
            clubsPk = []
            clubs = SportsClub.objects.filter(clubUser=sc_user)
            for club in clubs:
                clubsPk.append(club.pk)

            modeldata = Athlete.objects.filter(licenses__sportsClub__in=clubsPk).distinct()
            total = modeldata.count()

        elif user.groups.filter(name__in=['Yonetim', 'Admin']):
            modeldata = Athlete.objects.all()
            total = Athlete.objects.all().count()


    else:
        if search:
            modeldata =Athlete.objects.filter(
                Q(user__last_name__icontains=search) | Q(user__first_name__icontains=search) | Q(
                    user__email__icontains=search))
            total = modeldata.count();

        else:
            compAthlete=CompAthlete.objects.filter(competition=competition)
            athletes = []
            for comp in compAthlete:
                if comp.athlete:
                        athletes.append(comp.athlete.pk)
            if user.groups.filter(name='KulupUye'):
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                modeldata = Athlete.objects.exclude(pk__in=athletes).filter(licenses__sportsClub__in=clubsPk).distinct()[start:start + length]
                total = mAthlete.objects.exclude(pk__in=athletes).filter(licenses__sportsClub__in=clubsPk).distinct().count()
            elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                modeldata = Athlete.objects.exclude(pk__in=athletes)[start:start + length]
                total =Athlete.objects.exclude(pk__in=athletes).count()


    say = start + 1
    start = start + length
    page = start / length

    beka = []
    for item in modeldata:
        klup=''
        try:
            if item.licenses:
                for lisans in item.licenses.all():
                    if lisans.sportsClub:
                        klup = str(lisans.sportsClub) + "<br>" + klup
        except:
            klup=''



        data = {
            'say': say,
            'pk': item.pk,

            'name': item.user.first_name + ' ' + item.user.last_name,
             'birthDate':item.person.birthDate,

            'klup':klup,

        }
        beka.append(data)
        say += 1


    response = {

        'data': beka,
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,

    }
    return JsonResponse(response)


@login_required
def choose_athlete(request, pk, competition):
    perm = general_methods.control_access(request)
    login_user = request.user

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            user = User.objects.get(pk=login_user.pk)
            competition = Competition.objects.get(pk=competition)
            athlete = Athlete.objects.get(pk=pk)
            compAthlete = CompAthlete()
            compAthlete.athlete = athlete
            compAthlete.competition = competition
            compAthlete.total = request.POST.get('total')
            compAthlete.weight = request.POST.get('weight')
            compAthlete.save()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})











@login_required
def musabaka_sporcu_tamamla(request, athletes):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST':
        athletes1 = request.POST.getlist('selected_options')
        if athletes1:
            return redirect('sbs:musabaka-sporcu-tamamla', athletes=athletes1)
            # for x in athletes1:
            #
            #         athlete = Athlete.objects.get(pk=x)
            #         compAthlete = CompAthlete()
            #         compAthlete.athlete = athlete
            #         compAthlete.competition = competition
            #         compAthlete.save()
        else:
            messages.warning(request, 'Sporcu Seçiniz')

    return render(request, 'musabaka/musabaka-sporcu-tamamla.html', {'athletes': athletes})


@login_required
def musabaka_sporcu_sil(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            athlete = SandaAthlete.objects.get(pk=pk)
            athlete.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
