import csv

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.models import Permission, User, Group
from django.shortcuts import redirect

from wushu.models import Menu, MenuAdmin, MenuAthlete, MenuReferee, MenuCoach, MenuDirectory, MenuClubUser, \
    SportClubUser, Person, Athlete, Coach, Judge, DirectoryMember, SportsClub, Communication, City, Country, ClubRole


def getMenu(request):
    menus = Menu.objects.all()
    return {'menus': menus}


def getAdminMenu(request):
    adminmenus = MenuAdmin.objects.all()
    return {'adminmenus': adminmenus}


def getAthleteMenu(request):
    athletemenus = MenuAthlete.objects.all()
    return {'athletemenus': athletemenus}


def getRefereeMenu(request):
    refereemenus = MenuReferee.objects.all()
    return {'refereemenus': refereemenus}


def getCoachMenu(request):
    coachmenus = MenuCoach.objects.all()
    return {'coachmenus': coachmenus}


def getDirectoryMenu(request):
    directorymenus = MenuDirectory.objects.all()
    return {'directorymenus': directorymenus}


def getClubUserMenu(request):
    clubusermenus = MenuClubUser.objects.all()
    return {'clubusermenus': clubusermenus}


def show_urls(urllist, depth=0):
    urls = []

    # show_urls(urls.urlpatterns)
    for entry in urllist:

        urls.append(entry)
        perm = Permission(name=entry.name, codename=entry.pattern.regex.pattern, content_type_id=7)

        if Permission.objects.filter(name=entry.name).count() == 0:
            perm.save()
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

    return urls


def show_urls_deneme(urllist, depth=0):
    urls = []
    # show_urls(urls.urlpatterns)
    for entry in urllist:

        urls.append(entry)

        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

    return urls


def control_access(request):
    group = request.user.groups.all()[0]

    permissions = group.permissions.all()

    is_exist = False

    for perm in permissions:

        if request.resolver_match.url_name == perm.name:
            is_exist = True

    if group.name == "Admin":
        is_exist = True

    return is_exist


def control_access_klup(request):
    group = request.user.groups.all()[0]

    permissions = group.permissions.all()

    is_exist = False

    for perm in permissions:

        if request.resolver_match.url_name == perm.name:
            is_exist = True

    if group.name == "Admin" or group.name=="KulupUye":
        is_exist = True

    return is_exist


def getProfileImage(request):
    if (request.user.id):
        current_user = request.user

        if current_user.groups.filter(name='KulupUye').exists():
            athlete = SportClubUser.objects.get(user=current_user)
            person = Person.objects.get(id=athlete.person.id)

        elif current_user.groups.filter(name='Sporcu').exists():
            athlete = Athlete.objects.get(user=current_user)
            person = Person.objects.get(id=athlete.person.id)

        elif current_user.groups.filter(name='Antrenor').exists():
            athlete = Coach.objects.get(user=current_user)
            person = Person.objects.get(id=athlete.person.id)

        elif current_user.groups.filter(name='Hakem').exists():
            athlete = Judge.objects.get(user=current_user)
            person = Person.objects.get(id=athlete.person.id)

        elif current_user.groups.filter(name='Yonetim').exists():
            athlete = DirectoryMember.objects.get(user=current_user)
            person = Person.objects.get(id=athlete.person.id)

        elif current_user.groups.filter(name='Admin').exists():
            person = dict()
            person['profileImage'] = "profile/logo.png"

        else:
            person = None

        return {'person': person}

    return {}


def import_csv():
    doc_root = settings.BASE_DIR + '/media/wushu_csv.csv'
    with open(doc_root) as csv_file:
        file_reader = csv.reader(csv_file, delimiter=';')
        next(file_reader, None)  # skip the headers
        for row in file_reader:
            club = SportsClub()
            club.name = row[14]
            club.shortName = row[15]
            club.foundingDate = row[16]

            club.save()

            comClub = Communication()
            comClub.city = City.objects.get(name__icontains =row[18].strip())
            comClub.phoneNumber = row[17]
            comClub.address = row[19]
            comClub.country = Country.objects.get(name__icontains="TÜRKİYE")
            comClub.save()

            club.comminication = comClub

            club.save()


            user = User()
            user.first_name = row[1]
            user.last_name = row[2]
            user.username = row[10]

            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()

            user.groups.add(Group.objects.get(name='KulupUye'))
            user.save()

            person = Person()
            person.tc = row[0]
            person.motherName = row[3]
            person.fatherName = row[4]
            person.gender = row[5]
            person.birthDate = row[7]
            person.birthplace = row[6]
            person.bloodType = row[8]
            person.save()

            comClubUser = Communication()
            comClubUser.city = City.objects.get(name__icontains=row[12].strip())
            comClubUser.phoneNumber = row[11]
            comClubUser.address = row[13]
            comClubUser.country = Country.objects.get(name="TÜRKİYE")
            comClubUser.save()

            sportClubUser = SportClubUser()
            sportClubUser.person = person
            sportClubUser.user = user
            sportClubUser.communication = comClubUser
            sportClubUser.sportClub = club
            sportClubUser.role =ClubRole.objects.get(name__icontains=row[9].strip())

            sportClubUser.save()

            print(row)
