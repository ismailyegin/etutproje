from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
# from rest_framework_simplejwt import views as jwt_views
from django.http import JsonResponse

from sbs.models import SportClubUser, SportsClub, Coach, Level, License, Athlete, Person, Judge, EPProject, City
from sbs.services import general_methods
# from rest_framework.authtoken.models import Token


from datetime import date,datetime


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
    last_athlete = Athlete.objects.order_by('-creationDate')[:8]
    total_club = SportsClub.objects.all().count()
    total_athlete = Athlete.objects.all().count()
    total_athlete_gender_man=Athlete.objects.filter(person__gender=Person.MALE).count()
    total_athlete_gender_woman=Athlete.objects.filter(person__gender=Person.FEMALE).count()
    total_athlate_last_month=Athlete.objects.exclude(user__date_joined__month=datetime.now().month).count()
    total_club_user = SportClubUser.objects.all().count()
    total_coachs = Coach.objects.all().count()

    return render(request, 'anasayfa/admin.html',
                  {'total_club_user': total_club_user, 'total_club': total_club,
                   'total_athlete': total_athlete, 'total_coachs':total_coachs,'last_athletes':last_athlete,'total_athlete_gender_man':total_athlete_gender_man,
                   'total_athlete_gender_woman':total_athlete_gender_woman,'total_athlate_last_month':total_athlate_last_month,

                   })

@login_required
def City_athlete_cout(request):

    if request.method == 'POST' and request.is_ajax():
        try:
            totalprojects = EPProject.objects.filter(city__name__icontains=request.POST.get('city')).count()
            data = {
                'totalprojects': totalprojects

            }
            return JsonResponse(data)
        except Level.DoesNotExist:
            return JsonResponse({'status': 'Fail'})

    else:
        return JsonResponse({'status': 'Fail'})
#
#
