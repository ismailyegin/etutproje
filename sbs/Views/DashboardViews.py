from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
# from rest_framework_simplejwt import views as jwt_views
from django.http import JsonResponse

from sbs.models import SportClubUser, SportsClub, Coach, Level, License, Athlete, Person, Judge, EPProject, City
from sbs.models.EPProject import EPProject
from sbs.models.Employee import Employee
from sbs.services import general_methods
from django.db.models import Sum
from sbs.models.Message import Message
# from rest_framework.authtoken.models import Token


from datetime import date, datetime

from django.conf import settings


@login_required
def return_message(request):
    fdk = Message.objects.all()
    return render(request, 'Chat/chat.html')

@login_required
def return_athlete_dashboard(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    return render(request, 'anasayfa/sporcu.html')


@login_required
def return_referee_dashboard(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    return render(request, 'anasayfa/hakem.html')


@login_required
def return_coach_dashboard(request):
    perm = general_methods.control_access(request)
    #
    # if not perm:
    #     logout(request)
    #
    #     return redirect('accounts:login')
    return render(request, 'anasayfa/antrenor.html')


@login_required
def return_directory_dashboard(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    return render(request, 'anasayfa/federasyon.html')


@login_required
def return_club_user_dashboard(request):
    perm = general_methods.control_access(request)
    # x = general_methods.import_csv()

    if not perm:
        logout(request)
        return redirect('accounts:login')

    if not perm:
        logout(request)
        return redirect('accounts:login')

    belts = Level.objects.all()
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    current_user = request.user
    clubuser = SportClubUser.objects.get(user=current_user)
    club = SportsClub.objects.filter(clubUser=clubuser)[0]
    if user.groups.filter(name='KulupUye'):

        belts = Level.objects.filter(athlete__licenses__sportsClub=club)
    elif user.groups.filter(name__in=['Yonetim', 'Admin']):
        belts = Level.objects.all()

    total_club_user = club.clubUser.count()
    total_coach = Coach.objects.filter(sportsclub=club).count()
    sc_user = SportClubUser.objects.get(user=user)
    clubsPk = []
    clubs = SportsClub.objects.filter(clubUser=sc_user)
    for club in clubs:
        clubsPk.append(club.pk)
    total_athlete = Athlete.objects.filter(licenses__sportsClub__in=clubsPk).distinct().count()
    return render(request, 'anasayfa/kulup-uyesi.html',
                  {'total_club_user': total_club_user, 'total_coach': total_coach, 'belts': belts,
                   'total_athlete': total_athlete})


@login_required
def return_admin_dashboard(request):
    perm = general_methods.control_access(request)
    # x = general_methods.import_csv()




    if not perm:
        logout(request)
        return redirect('accounts:login')

    if not perm:
        logout(request)
        return redirect('accounts:login')
    # son eklenen 8 sporcuyu ekledik
    last_employee = Employee.objects.order_by('-creationDate')[:5]
    personel_count=Employee.objects.count()
    proje_count=EPProject.objects.count()



    proje_status_PT=EPProject.objects.filter(projectStatus=EPProject.PT).distinct().count()
    proje_status_PDE=EPProject.objects.filter(projectStatus=EPProject.PDE).distinct().count()
    proje_status_PD = EPProject.objects.filter(projectStatus=EPProject.PD).distinct().count()
    proje_status_PIE = EPProject.objects.filter(projectStatus=EPProject.PIE).distinct().count()

    cezainfaz=EPProject.objects.filter(projeCinsi=EPProject.CIK).count()
    adaletbinasi=EPProject.objects.filter(projeCinsi=EPProject.AB).count()
    adlitip=EPProject.objects.filter(projeCinsi=EPProject.AT).count()
    bolgeadliye=EPProject.objects.filter(projeCinsi=EPProject.BAM).count()
    bolgeidari=EPProject.objects.filter(projeCinsi=EPProject.BIM).count()
    denetimserbeslik=EPProject.objects.filter(projeCinsi=EPProject.DS).count()
    personelegitim=EPProject.objects.filter(projeCinsi=EPProject.PEM).count()
    bakanlikbinasi=EPProject.objects.filter(projeCinsi=EPProject.BB).count()
    diger=EPProject.objects.filter(projeCinsi=EPProject.DIGER).count()
    lojman=EPProject.objects.filter(projeCinsi=EPProject.LOJMAN).count()







    cezainfaz_sum = int(EPProject.objects.filter(projeCinsi=EPProject.CIK).distinct().aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    adaletbinasi_sum =int(EPProject.objects.filter(projeCinsi=EPProject.AB).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    adlitip_sum = int(EPProject.objects.filter(projeCinsi=EPProject.AT).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    bolgeadliye_sum = int(EPProject.objects.filter(projeCinsi=EPProject.BAM).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    bolgeidari_sum = int(EPProject.objects.filter(projeCinsi=EPProject.BIM).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    denetimserbeslik_sum = int(EPProject.objects.filter(projeCinsi=EPProject.DS).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    personelegitim_sum = int(EPProject.objects.filter(projeCinsi=EPProject.PEM).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    bakanlikbinasi_sum = int(EPProject.objects.filter(projeCinsi=EPProject.BB).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    diger_sum = int(EPProject.objects.filter(projeCinsi=EPProject.DIGER).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)
    lojman_sum = int(EPProject.objects.filter(projeCinsi=EPProject.LOJMAN).aggregate(Sum('insaatAlani'))['insaatAlani__sum'] or 0)

    projects = EPProject.objects.all().distinct()
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








    return render(request, 'anasayfa/admin.html',
                  {'employees': last_employee,
                   'personel_count': personel_count,
                   'proje_count': proje_count,
                   'proje_status_PT': proje_status_PT,
                   'proje_status_PDE': proje_status_PDE,
                   'proje_status_PD': proje_status_PD,
                   'proje_status_PIE': proje_status_PIE,
                   'cezainfaz':cezainfaz,
                   'adaletbinasi':adaletbinasi,
                   'adlitip':adlitip,
                   'bolgeadliye':bolgeadliye,
                   'bolgeidari':bolgeidari,
                   'denetimserbeslik':denetimserbeslik,
                   'personelegitim':personelegitim,
                   'bakanlikbinasi':bakanlikbinasi,
                   'diger':diger,'lojman':lojman,

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
def City_athlete_cout(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            login_user = request.user
            user = User.objects.get(pk=login_user.pk)
            projects = EPProject.objects.none()
            city = City.objects.get(name__icontains=request.POST.get('city'))


            if user.groups.filter(name__in=['Teknik', 'Admin']):

                projects = EPProject.objects.filter(city__name__icontains=city)


            elif user.groups.filter(name='Personel'):
                projects = EPProject.objects.filter(employees__employee__user=user).distinct()
                projects |= EPProject.objects.filter(sorumlu__user=user).distinct()



            totalprojects = projects.filter(city__name__icontains=request.POST.get('city')).count()

            data = {
                'totalprojects': totalprojects,
                'cityid': city.pk

            }
            return JsonResponse(data)
        except Level.DoesNotExist:
            return JsonResponse({'status': 'Fail'})

    else:
        return JsonResponse({'status': 'Fail'})
#
#
