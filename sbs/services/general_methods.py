import csv
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import Permission, User, Group
from django.core.mail import EmailMultiAlternatives

from sbs.models.City import City
from sbs.models.ClubRole import ClubRole
from sbs.models.Communication import Communication
from sbs.models.Country import Country
from sbs.models.DirectoryMember import DirectoryMember
from sbs.models.Employee import Employee
from sbs.models.Logs import Logs
from sbs.models.Menu import Menu
from sbs.models.MenuAdmin import MenuAdmin
from sbs.models.MenuDirectory import MenuDirectory
from sbs.models.MenuPersonel import MenuPersonel
from sbs.models.MenuTeknik import MenuTeknik
from sbs.models.Message import Message
from sbs.models.Notification import Notification
from sbs.models.Person import Person
from sbs.models.SportClubUser import SportClubUser
from sbs.models.SportsClub import SportsClub


def getMenu(request):
    menus = Menu.objects.all()
    return {'menus': menus}


def getAdminMenu(request):
    adminmenus = MenuAdmin.objects.all()

    return {'adminmenus': adminmenus}

def getPersonelMenu(request):
    personelmenus = MenuPersonel.objects.all()
    return {'personelmenus': personelmenus}



def getTeknikMenu(request):
    teknikmenus = MenuTeknik.objects.all().order_by('count')
    return {'teknikmenus': teknikmenus}



def getDirectoryMenu(request):
    directorymenus = MenuDirectory.objects.all()
    return {'directorymenus': directorymenus}





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

def control_access_personel(request):
    group = request.user.groups.all()[0]

    permissions = group.permissions.all()

    is_exist = False

    for perm in permissions:

        if request.resolver_match.url_name == perm.name:
            is_exist = True

    if group.name == "Admin" or group.name=="Personel" or group.name=="Teknik" :
        is_exist = True

    return is_exist

def control_access_technical(request):
    group = request.user.groups.all()[0]

    permissions = group.permissions.all()

    is_exist = False

    for perm in permissions:

        if request.resolver_match.url_name == perm.name:
            is_exist = True

    if group.name == "Admin" or group.name=="Teknik":
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

        if current_user.groups.filter(name='Personel').exists():
            personel = Employee.objects.get(user=current_user)
            person = Person.objects.get(id=personel.person.id)


        elif current_user.groups.filter(name='Teknik').exists():
            personel = Employee.objects.get(user=current_user)
            person = Person.objects.get(id=personel.person.id)

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


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def logwrite(request, log):
    try:
        logs = Logs(user=request.user, subject=log, ip=get_client_ip(request))
        logs.save()

        # f = open("log.txt", "a")
        #log = get_client_ip(request) + "    [" + datetime.today().strftime('%d-%m-%Y %H:%M') + "] " + str(user) + " " + log + " \n "
        # f.write(log)
        # f.close()

    except Exception as e:
        print('log write hata var ')
        # f = open("log.txt", "a")
        log = "[" + datetime.today().strftime('%d-%m-%Y %H:%M') + "] hata   \n "
        # f.write(log)
        # f.close()
    return log





def get_notification(request):
    if (request.user.id):
        notifications = Notification.objects.filter(users=request.user).order_by("-creationDate")[:10]
        say = Notification.objects.filter(users=request.user, is_show=False).count()

        return {
            'notifications': notifications,
            'notificationsCount': say,
        }

    return {}


class Messages:
    def __init__(self, body, user, creationDate, is_show, chat_id, image, username):
        self.body = body
        self.user = user
        self.creationDate = creationDate
        self.is_show = is_show
        self.chat_id = chat_id
        self.image = image
        self.username = username



def get_message(request):
    if (request.user):
        # # mesaj gönderenler
        #         # query = 'Select * from  sbs_message where recipient_id=%s  group by user_id order by creationDate desc' %request.user.pk
        #         # messagesIn = Message.objects.raw(query)
        #         # # mesaj gönderdiklerim
        #         # query = 'Select * from  sbs_message where user_id=%s  group by recipient_id order by creationDate desc' % request.user.pk
        #         # messagesOut= Message.objects.raw(query)
        #         # list = []
        #         # for item in messagesIn:
        #         #     query='Select * from  sbs_message where (user_id=%s and   recipient_id=%s) or  (user_id=%s and   recipient_id=%s) order by creationDate desc LIMIT 1' % (request.user.pk,item.user.pk,item.user.pk,request.user.pk)
        #         #     message=Message.objects.raw(query)
        #         #     for m in message:
        #         #         list.append(m.pk)
        #         # for item in messagesOut:
        #         #     query='Select * from  sbs_message where (user_id=%s and   recipient_id=%s) or  (user_id=%s and   recipient_id=%s) order by creationDate desc LIMIT 1' % (request.user.pk,item.recipient.pk,item.recipient.pk,request.user.pk)
        #         #     message = Message.objects.raw(query)
        #         #     for m in message:
        #         #         list.append(m.pk)
        #         #
        #         # messages=Message.objects.none()
        #         # for item in list:
        #         #     messages|= Message.objects.filter(pk=item)
        #         # messages=messages.distinct().order_by('-creationDate')

        # query = 'select * from (SELECT * FROM etutproje.sbs_message where user_id=%s or recipient_id=%s order by creationDate desc limit 10000) as t group by chat_id' % (
        #     request.user.pk, request.user.pk)
        # messages = list(Message.objects.raw(query))
        messages = Message.objects.none()
        mesaj = []
        for item in messages:

            message = Message.objects.get(pk=int(item.id))
            image = ''
            username = ''

            # if message.user.groups.filter(name='Personel').exists():
            # :

            # benim gönderdigim mesaj
            if (request.user == message.user):
                if message.recipient.groups.filter(name='Personel').exists() or message.recipient.groups.filter(
                        name='Teknik').exists():
                    image = Employee.objects.get(user=message.recipient).person.profileImage
                    username = Employee.objects.get(user=message.recipient).user.username
                elif message.recipient.groups.filter(name='Admin').exists():
                    image = 'profile/logo.png'
                    username = 'admin'

                user = message.recipient.get_full_name()
                is_show = True


            # bana gelen mesaj
            else:
                if message.user.groups.filter(name='Personel').exists() or message.user.groups.filter(
                        name='Teknik').exists():
                    image = Employee.objects.get(user=message.user).person.profileImage
                    username = Employee.objects.get(user=message.user).user.username

                elif message.user.groups.filter(name='Admin').exists():
                    image = 'profile/logo.png'
                    username = 'admin'

                user = message.user.get_full_name()
                is_show = message.is_show

            mesaj.append(Messages(message.body,
                                  user,
                                  message.creationDate,
                                  is_show,
                                  str(message.chat_id),
                                  image,
                                  username))

        # say = len(list(Message.objects.raw(
        #     'select * from (select * from (SELECT * FROM etutproje.sbs_message where  recipient_id=%s order by creationDate desc limit 10000) as t group by chat_id) as x where x.is_show=0;' % (
        #         request.user.pk))))
        return {
            'messages': mesaj,
            # 'messageCount': say,
        }
    else:
        return {}


    return {}

def mailsend(request):
    #gonderilecek kisinin mail adresi ve içerik gelecek
    mail = request.POST.get('username')
    subject, from_email, to = 'THF Bilgi Sistemi Kullanıcı Bilgileri', 'no-reply@thf.gov.tr', mail
    html_content = '<h2>ADALET BAKANLIGI PROJE TAKİP  SİSTEMİ</h2>'
    html_content = html_content + '<p><strong>gonderilecek veri:</strong></p>'

    msg = EmailMultiAlternatives(subject, '', from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return {}