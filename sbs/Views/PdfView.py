

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect





from sbs.models import EPProject, CategoryItem, City
from sbs.models.CategoryItem import  CategoryItem
from sbs.models.Town import Town
from sbs.models.Employee import Employee

from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse




# pdf
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak



# resim

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from oxiterp.settings.base import MEDIA_URL



import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.units import inch

from reportlab.pdfbase.pdfmetrics import registerFontFamily




# zaman
import datetime
from django.utils import timezone

# excel
import csv
import xlwt


@login_required

def return_pdf2(request):



    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ProjeTakip.pdf"'
    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    logo = ImageReader('https://www.google.com/images/srpr/logo11w.png')
    c.drawImage(logo, 100, 100, width=None,height=None,mask=None)
    c.showPage()
    c.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(c)

    return response




@login_required

def html_to_pdf_view(request):

    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    logo = ImageReader('https://www.google.com/images/srpr/logo11w.png')
    c.drawImage(logo, 50, 50, width=None, height=None, mask='auto')
    c.setFont("Times-Roman",12)
    for  item  in range(100,10000,100):
        c.drawString(100,item, 'Proje Takip Programi')


    c.showPage()

    c.save()
    buffer.seek(0)




    return FileResponse(buffer, as_attachment=True, filename='Personeller.pdf')


@login_required
def return_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ProjeTakip.pdf"'

    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    c.setTitle('Title Proje Takip ')

    for i in range(5):
        page_num = c.getPageNumber()
        # text = "Proje Takip Programi %s" % page_num
        c.setFont("Times-Roman", 28)
        text = "Proje Takip Programi "
        c.drawString(150, 750, text)
        c.line(50, 650, 550, 650)
        c.showPage()
    c.save()



    # c.drawString(150, 800, 'Proje Takip Programi')


    # c.beginForm("SpumoniForm")

    # c.showPage()
    # c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


@login_required
def return_excel_row_personel(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Tc', 'İsim', 'Ünvan', 'Email']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    employee = Employee.objects.all().distinct()



    row=1
    for item in employee:
         ws.write(row, 0, item.person.tc, font_style)
         ws.write(row, 1, item.user.get_full_name(), font_style)
         ws.write(row, 2, item.workDefinition.name, font_style)
         ws.write(row, 3, item.user.email, font_style)

         row=row+1



    wb.save(response)
    return response



@login_required
def return_excel_row(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Username', 'First name', 'Last name', 'Email address', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response



@login_required
def return_excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    # writer.writerow(['Username', 'First name', 'Last name', 'Email address'])

    users = User.objects.all()
    for user in users:
        writer.writerow([user.username])
        writer.writerow([user.first_name])
        writer.writerow([user.last_name])
        writer.writerow([user.email])
    return response







@login_required
def edit_project_pdf(request,pk):
    project = EPProject.objects.get(pk=pk)
    text=""
    text=request.GET.get('get')


    days = None
    if project.aifinish:
        days = (project.aifinish - timezone.now()).days


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ProjeTakip.pdf"'
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.setTitle('Etüt Proje')

    logo = ImageReader("http://kobiltek.com:81/etutproje/media/profile/logo.png")
    c.drawImage(logo, 460, 740, width=80, height=80, mask='auto')
    # for i in range(5):
    #     page_num = c.getPageNumber()
    #     # text = "Proje Takip Programi %s" % page_num

    # data = "ğçİöşü"
    # p = Paragraph(data.decode('utf-8'), style=styNormal)

    # c.setFont("Times-Roman", 32)





    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))

    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))


    c.setFont("Verdana", 8)

    c.drawString(50, 800, " Rapor Tarih:" )

    c.drawString(105, 800, "%s" % datetime.datetime.today().strftime('%d-%m-%Y %H:%M'))

    c.setFont("Verdana", 16)
    c.drawString(100,770,'DESTEK HİZMETLERİ DAİRE BAŞKANLIĞI ')
    c.drawString(120, 745, ' ETÜT PROJE ŞUBE MÜDÜRLÜĞÜ')

    c.setFont("Verdana", 15)
    name=''
    count=1
    control=True
    kelime=''
    for item  in project.name:
        kelime+=item

        if count==58:
            c.drawString(50, 720, "%s" % name)
            name = ''
        elif count==116:
            c.drawString(50, 700, "%s" % name)
            name = ''
            control=False

        if item ==' ':
            name+=' '
            name+=kelime
            kelime=''


        if len(project.name)==count:
            name+=' '
            name+=kelime
        count=count+1
    if control:
        c.drawString(50, 700, "%s" % name)
    else:
        c.drawString(50, 680, "%s" % name)




    # c.line(50, 720, 550, 720)

    c.setFont("Verdana", 15)
    c.drawString(50,650,'Genel Bilgiler')
    c.line(50, 640, 470, 640)



    c.setFont("Verdana", 10)
    c.drawString(50,620,"İl                       :%s" %project.city)
    if project.town:
        c.drawString(50,600,"İlçe                    :%s" %project.town)
    else:
        c.drawString(50, 600, "İlçe                    :%s" % project.town)
    c.drawString(50,580,"Yatırım Programı :%s" %project.butceCinsi)
    c.drawString(50,560,"Bütçe Yılı            :%s" %project.butceYili)

    x = 540

    if project.phases.all().order_by('phaseDate').last():
        name = ''
        count = 0
        control = True
        kelime = ''
        say = 0
        for item in str(project.phases.all().order_by('phaseDate').last()):

            count = count + 1

            kelime += item
            if item == ' ':

                name += ' '
                name += kelime
                kelime = ''

            if len(str(project.phases.all().order_by('phaseDate').last())) == count:

                name += ' '
                name += kelime
                kelime = ' '
            if count % 60 == 0:

                if say == 0:
                    c.setFont("Verdana", 10)
                    c.drawString(50, x - 10 * say, "Projenin Aşaması:%s" % name)
                else:
                    c.setFont("Verdana", 10)
                    c.drawString(50, x - 10 * say, "%s" % name)
                name = ' '
                say += 1

        if control:

            if say == 0:
                c.setFont("Verdana", 10)
                c.drawString(50, x - say * 10, "Projenin Aşamasi:%s" % name)
                name = ' '

            else:
                c.setFont("Verdana", 10)
                c.drawString(50, x - say * 10, "%s" % name)
                name = ' '

        else:
            c.setFont("Verdana", 10)
            c.drawString(50, x - say * 10, "Projenin Aşamasi%s" % name)

        x = x - say * 10
    else:
        c.drawString(50, x, '')
        x = x - 20;



    c.drawString(300,620,"Projenin Cinsi          :%s" %project.projeCinsi)
    c.drawString(300,600,"Karakteristik           :%s" %project.karakteristik)
    c.drawString(300,580,"Projenin Durumu     :%s" %project.projectStatus)

    if project.sorumlu:
        c.drawString(300,560,"Projenin Sorumlusu :%s" %project.sorumlu  )
    else:
        c.drawString(300, 560, "Projenin Sorumlusu:")


    c.setFont("Verdana", 15)
    c.drawString(50, x - 20, 'İhale Bilgileri')  # 520
    c.line(50, x - 30, 200, x - 30)  # 510
    c.setFont("Verdana", 10)
    x = x - 50

    c.drawString(50, x, "İhale Tarihi                         :%s" % (
        project.ihaleTarihi.strftime('%d/%m/%Y') if project.ihaleTarihi else ' '))
    c.drawString(50, x - 20, "Sözleşme Tarihi                  :%s" % (
        project.sozlesmeTarihi.strftime('%d/%m/%Y') if project.sozlesmeTarihi else ' '))
    c.drawString(50, x - 40, "Alım İşinin Başlangıç Tarihi  :%s" % (
        project.aistart.strftime('%d/%m/%Y') if project.aistart else ' '))
    c.drawString(50, x - 60, "Alım İşinin Bitiş Tarihi         :%s" % (
        project.aifinish.strftime('%d/%m/%Y') if project.aifinish else ' '))
    c.drawString(50, x - 80,
                 "İşin Süresi                         :%s (Gün)" % (project.isSUresi if project.isSUresi else ' '))
    #
    if project.projectStatus == EPProject.PT:
        c.drawString(50, x - 100, "Kaç Gün Kaldi                    :Proje Tamamlandı")


    elif project.projectStatus == EPProject.PIE:
        c.drawString(50, x - 100, "Kaç Gün Kaldi                    :Proje İptal Edildi")


    else:
        c.drawString(50, x - 100, "Kaç Gün Kaldi                    :%s (Gün)" % (days if days else ' '))

    c.setFont("Verdana", 10)
    c.drawString(50, x - 120, "Sözleşme Bedeli                :%s  TL" % (
        "{:,}".format(project.sozlesmeBedeli) if project.sozlesmeBedeli else '  '))
    c.drawString(50, x - 140, "Sözleşme Bedeli Kdv Dahil  :%s TL" % (
        "{:,}".format(project.sozlesmeBedeliKdv) if project.sozlesmeBedeliKdv else '  '))

    c.drawString(50, x - 160, 'Firma :%s' % (
        project.company if project.company else ' '))
    # c.drawString(50, x - 180, 'İhale Müellif                      :%s' % project.ihalemuellif)
    # c.drawString(50, x - 200, 'İletişim (email)                  :%s' % project.ihaleimail)
    # c.drawString(50, x - 220, 'İletişim (tel)                      :%s' % project.ihaletel)




    c.setFont("Verdana", 15)
    c.drawString(300, x + 30, 'Arsa Yapım Ödenek Bilgileri')
    c.line(300, x + 20, 450, x + 20)
    c.setFont("Verdana", 10)

    c.drawString(300, x, "Arsa Alanı                    :%s m²" % (
        "{0:,.2f}".format(project.arsaAlani) if project.arsaAlani else ' '))

    c.drawString(300, x - 20, "İnşaat Alanı                 :%s m² " % (
        "{0:,.2f}".format(project.insaatAlani) if project.insaatAlani else ' '))
    c.drawString(300, x - 40, "Tahmini Ödenek Tutari :%s TL" % (
        "{0:,.2f}".format(project.tahminiOdenekTutari) if project.tahminiOdenekTutari else ' '))
    # c.drawString(300, 500, "Yaklaşık Maliyet           :%s " % ("{0:,.2f}".format(project.yaklasikMaliyet) if project.yaklasikMaliyet else  ' ' ))

    y = x -60

    if  project.employees.all():
        c.setFont("Verdana", 15)
        c.drawString(300, y, 'Personel Listesi:')
        y-=10
        c.line(300, y, 450, y)
        c.setFont("Verdana", 10)

        # c.setFillColorRGB(0, 0, 0.77)
        y-=20

        c.drawString(300, y, 'İsim-Soyisim')

        c.line(300, y-10, 350, y-10)

        c.drawString(420, y, 'Kontrol Alanı')
        c.line(420, y - 10, 470, y - 10)

        # c.setFillColorRGB(0, 0, 0)

        for item in project.employees.all():

            if y > 150:

                y -= 20
                c.drawString(300, y, '%s' % item.employee)
                c.drawString(420, y, '%s' % item.projectEmployeeTitle)

            else:
                page_num = c.getPageNumber()
                c.showPage()
                pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
                # c.drawString(50, 25, 'http:/www.kobiltek.com/')
                # c.drawString(450, 25, 'Proje Takip Sistemi')
                page_num = c.getPageNumber()
                # c.drawString(280, 25, '%s' % page_num)
                y = 750

        page_num = c.getPageNumber()
        #
        # c.drawString(50, 25, 'http:/www.kobiltek.com/')
        # c.drawString(280, 25, '%s' % page_num)
        # c.drawString(450, 25, 'Proje Takip Sistemi')

    # y=x-160
    print(x)
    if project.vest.all():
        # 160
        c.setFont("Verdana", 15)

        c.drawString(50, x - 180, 'Hakediş Bilgileri')

        c.setFont("Verdana", 10)

        c.line(50, x - 190, 200, x - 190)
        c.drawString(50, x - 210, 'Tarihi  ')
        c.line(50, x - 220, 100, x - 220)

        c.drawString(150, x - 210, 'Miktarı')
        c.line(150, x - 220, 200, x - 220)

        y = x - 240
        for item in project.vest.all():

            if y > 50:
                c.drawString(50, y, '%s' % item.vestDate.strftime('%d/%m/%Y') if item.vestDate else '  ')
                c.drawString(150, y, '%s TL ' % ("{0:,.2f}".format(int(item.vest)) if int(item.vest) else '  '))
                y -= 20
            else:
                page_num = c.getPageNumber()
                c.showPage()
                pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))

                page_num = c.getPageNumber()
                # c.drawString(280, 25, '%s.Sayfa' % page_num)

                y = 750


    if project.requirements.all():
        y = y - 20

        c.setFont("Verdana", 15)
        c.drawString(50, y, 'İhtiyaç Listesi ')
        y = y - 10
        c.line(50, y, 200, y)
        c.setFont("Verdana", 10)
        y = y - 20
        c.drawString(50, y, 'Tanımı ')
        c.drawString(150, y, 'Adet')
        y = y - 10
        c.line(50, y, 100, y)
        c.line(150, y, 200, y)
        y = y - 20
        for item in project.requirements.all():
            if y > 150:
                c.drawString(50, y, '%s' % item.definition)
                c.drawString(150, y, '%s' % item.amount)
                y -= 20
            else:
                page_num = c.getPageNumber()
                c.showPage()
                pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
                # c.drawString(50, 25, 'http:/www.kobiltek.com/')
                # c.drawString(450, 25, 'Proje Takip Sistemi')
                page_num = c.getPageNumber()
                # c.drawString(280, 25, '%s.Sayfa' % page_num)

                y = 750

    # if project.offers.all():
    #     c.setFont("Verdana", 15)
    #     c.drawString(50, y, 'Görüş ve Öneriler:')
    #     y -= 10
    #     c.line(50, y, 150, y)
    #     c.setFont("Verdana", 10)
    #
    #     # c.setFillColorRGB(0, 0, 0.77)
    #     #   y440
    #     y -= 20
    #     c.drawString(50, y, 'İsim-Soyisim')
    #     c.line(50, y - 10, 100, y - 10)
    #
    #     c.drawString(150, y, 'Görüş ')
    #     c.line(150, y - 10, 200, y - 10)
    #     y -= 20
    #     for item in project.offers.all().order_by('creationDate')[:3]:
    #         if y > 150:
    #             c.drawString(50, y, '%s' % item.added_by)
    #             c.drawString(150, y, '%s' % item.message)
    #             y -= 20
    #         else:
    #             page_num = c.getPageNumber()
    #             c.showPage()
    #             pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    #             # c.drawString(50, 25, 'http:/www.kobiltek.com/')
    #             # c.drawString(450, 25, 'Proje Takip Sistemi')
    #             page_num = c.getPageNumber()
    #             # c.drawString(280, 25, '%s' % page_num)
    #             y = 750
    #
    #     page_num = c.getPageNumber()

    c.setFont("Verdana", 12)

    if text and text is not None:
        c.drawString(300, 150, 'Sayın  %s:' % text)
        c.drawString(300,130,'Bilgilerinize arz olunur.')
    # else:

        # c.drawString(300, 150, 'Sayın:.............')
        # c.drawString(300, 130, 'Bilgilerinize arz olunur.')


    c.showPage()

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response




@login_required
def edit_project_excel(request,pk):
    project = EPProject.objects.get(pk=pk)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="proje.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Projenin Tanimi', 'Bütçe yılı  ', 'Projenin Süresi ', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    ws.write(1, 0,project.name, font_style)
    ws.write(1, 1,project.butceYili, font_style)
    ws.write(1, 2,project.isSUresi, font_style)
    # ws.write(1, 3,project.sozlesmeBedeli, font_style)

    # for row in rows:
    #     row_num += 1
    #     for col_num in range(len(row)):
    #         ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def control(say1,say2):
    return say1+say2



@login_required
def edit_project_pdf_personel(request,pk):




    text=""
    text=request.GET.get('get')
    project = EPProject.objects.get(pk=pk)

    days = None
    if project.aifinish:
        days = (project.aifinish - timezone.now()).days

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ProjeTakip.pdf"'
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.setTitle('Etüt Proje ')

    logo = ImageReader('http://kobiltek.com:81/etutproje/'+MEDIA_URL + "profile/logo.png")
    c.drawImage(logo, 460, 730, width=80, height=80, mask='auto')
    # for i in range(5):
    #     page_num = c.getPageNumber()
    #     # text = "Proje Takip Programi %s" % page_num

    # data = "ğçİöşü"
    # p = Paragraph(data.decode('utf-8'), style=styNormal)

    # c.setFont("Times-Roman", 32)





    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))

    c.setFont("Verdana", 8)

    c.drawString(50, 800, " Rapor Tarih:" )

    c.drawString(105, 800, "%s" % datetime.datetime.today().strftime('%d-%m-%Y %H:%M'))



    c.setFont("Verdana", 16)
    c.drawString(100,770,'DESTEK HİZMETLERİ DAİRE BAŞKANLIĞI ')
    c.drawString(120, 745, ' ETÜT PROJE ŞUBE MÜDÜRLÜĞÜ')






    c.setFont("Verdana", 15)
    name=''
    count=1
    control=True
    kelime=''
    for item  in project.name:
        kelime+=item

        if count==58:
            c.drawString(50, 720, "%s" % name)
            name = ''
        elif count==116:
            c.drawString(50, 700, "%s" % name)
            name = ''
            control=False

        if item ==' ':
            name+=' '
            name+=kelime
            kelime=''


        if len(project.name)==count:
            name+=' '
            name+=kelime
        count=count+1
    if control:
        name
        c.drawString(50, 700, "%s" % name)
    else:
        c.drawString(50, 680, "%s" % name)




    # c.line(50, 720, 550, 720)

    c.setFont("Verdana", 15)
    c.drawString(50,650,'Genel Bilgiler')
    c.line(50, 640, 470, 640)



    c.setFont("Verdana", 10)
    c.drawString(50,620,"İl                       :%s" %project.city)
    if project.town:
        c.drawString(50,600,"İlçe                    :%s" %project.town)
    else:
        c.drawString(50, 600, "İlçe                    :%s" % project.town)
    c.drawString(50,580,"Yatırım Programı :%s" %project.butceCinsi)
    c.drawString(50,560,"Bütçe Yılı            :%s" %project.butceYili)
    # c.drawString(50, 540, "Projenin Aşaması :%s" % project.phases.all().order_by(
    #     'phaseDate').last() if project.phases.all().order_by('phaseDate').last() else ' ')



    c.drawString(300,620,"Projenin Cinsi          :%s" %project.projeCinsi)
    c.drawString(300,600,"Karakteristik           :%s" %project.karakteristik)
    c.drawString(300,580,"Projenin Durumu     :%s" %project.projectStatus)

    if project.sorumlu:
        c.drawString(300,560,"Projenin Sorumlusu :%s" %project.sorumlu  )
    else:
        c.drawString(300, 560, "Projenin Sorumlusu:")



    if project.requirements.all():
        c.setFont("Verdana", 15)
        c.drawString(50, 520, 'İhtiyaç Listesi ')
        c.line(50, 510, 200, 510)
        c.setFont("Verdana", 10)

        c.drawString(50, 500, 'Tanımı ')
        c.line(50, 490, 100, 490)

        c.drawString(150, 500, 'Adet')
        c.line(150, 490, 200, 490)

        y = 470

        # page_num = c.getPageNumber()
        # c.drawString(280, 25, '%s.Sayfa' % page_num)
        for item in project.requirements.all():
            if y > 150:
                c.drawString(50, y, '%s' % item.definition)
                c.drawString(150, y, '%s' % item.amount)
                y -= 20
            else:
                page_num = c.getPageNumber()
                c.showPage()
                pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
                # c.drawString(50, 25, 'http:/www.kobiltek.com/')
                c.drawString(450, 25, 'Proje Takip Sistemi')
                # page_num = c.getPageNumber()
                # c.drawString(280, 25, '%s.Sayfa' % page_num)

                y = 750

    # c.setFont("Verdana", 15)
    # c.drawString(50,590,'İhale Bilgileri')
    # c.line(50, 580, 200, 580)
    # c.setFont("Verdana", 10)
    #
    # c.drawString(50, 560, "İhale tarihi                         :%s" % (project.ihaleTarihi.strftime('%m/%d/%Y') if project.ihaleTarihi else  '-'))
    # c.drawString(50, 540, "Sözleşme tarihi                  :%s" %(project.sozlesmeTarihi.strftime('%m/%d/%Y')  if project.sozlesmeTarihi else  '-' ))
    # c.drawString(50, 520, "Alım İşinin Başlangıç tarihi  :%s" %(project.aistart.strftime('%m/%d/%Y')  if project.aistart else  '-' ))
    # c.drawString(50, 500, "Alım İşinin Bitiş tarihi         :%s"%(project.aifinish.strftime('%m/%d/%Y')  if project.aifinish else  '-' ))
    # c.drawString(50, 480, "İşin Süresi                         :%s" % (project.isSUresi if project.isSUresi else  '-' ))
    # c.drawString(50, 460, "Kaç Gün kaldi                    :%s" % (days if days else  '-' ))
    # c.setFont("Verdana", 15)
    # c.drawString(300,590,'Arsa Yapım Ödenek Bilgileri')
    # c.line(300, 580, 450, 580)
    # c.setFont("Verdana", 10)
    #
    #
    #
    #
    # c.drawString(300, 560, "Arsa Alanı                    :%s" % ("{0:,.2f}".format(project.arsaAlani) if project.arsaAlani else  '-' ))
    #
    #
    #
    # c.drawString(300, 540, "İnşaat alanı                 :%s" % ( "{0:,.2f}".format(project.insaatAlani) if project.insaatAlani else  '-' ))
    # c.drawString(300, 520, "Tahmini Ödenek Tutari :%s" % ("{0:,.2f}".format(project.tahminiOdenekTutari) if project.tahminiOdenekTutari else  '-' ))
    # c.drawString(300, 500, "Yaklaşık Maliyet           :%s" % ("{0:,.2f}".format(project.yaklasikMaliyet) if project.yaklasikMaliyet else  '-' ))



    y=540
    if project.offers.all():
        c.setFont("Verdana", 15)
        c.drawString(300, y, 'Görüş ve Öneriler:')
        y-=10
        c.line(300, y, 450, y)
        c.setFont("Verdana", 10)

        # c.setFillColorRGB(0, 0, 0.77)
        #   y440
        y-=20
        c.drawString(300, y, 'İsim-Soyisim')
        c.line(300, y-10, 350, y-10)

        c.drawString(400, y, 'Görüş ')
        c.line(400, y-10, 450, y-10)
        y-=20
        for item in project.offers.all().order_by('creationDate')[:3]:
            if y > 150:
                c.drawString(300, y, '%s' % item.added_by)
                c.drawString(400, y, '%s' % item.message)
                y -= 20
            else:
                page_num = c.getPageNumber()
                c.showPage()
                pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
                # c.drawString(50, 25, 'http:/www.kobiltek.com/')
                # c.drawString(450, 25, 'Proje Takip Sistemi')
                page_num = c.getPageNumber()
                # c.drawString(280, 25, '%s' % page_num)
                y = 750

        page_num = c.getPageNumber()

    if  project.employees.all():
        c.setFont("Verdana", 15)
        c.drawString(300, y, 'Personel Listesi:')
        y-=10
        c.line(300, y, 450, y)
        c.setFont("Verdana", 10)

        # c.setFillColorRGB(0, 0, 0.77)
        y-=20

        c.drawString(300, y, 'İsim-Soyisim')

        c.line(300, y-10, 350, y-10)

        c.drawString(400, y, 'Kontrol Alanı')
        c.line(400, y-10, 450, y-10)

        # c.setFillColorRGB(0, 0, 0)

        y -=20

        for item in project.employees.all():

            if y > 150:
                c.drawString(300, y, '%s' % item.employee)
                c.drawString(400, y, '%s' % item.projectEmployeeTitle)
                y -= 20
            else:
                page_num = c.getPageNumber()
                c.showPage()
                pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
                # c.drawString(50, 25, 'http:/www.kobiltek.com/')
                # c.drawString(450, 25, 'Proje Takip Sistemi')
                page_num = c.getPageNumber()
                # c.drawString(280, 25, '%s' % page_num)
                y = 750

        page_num = c.getPageNumber()
        #
        # c.drawString(50, 25, 'http:/www.kobiltek.com/')
        # c.drawString(280, 25, '%s' % page_num)
        # c.drawString(450, 25, 'Proje Takip Sistemi')

    # c.setFont("Verdana", 15)
    # c.drawString(50,440,'Hakediş Bilgileri')
    # c.line(50, 430, 200, 430)
    # c.setFont("Verdana", 10)
    #
    #
    # c.drawString(50, 410, "Sözleşme bedeli               :%s" % ( "{:,}".format(project.sozlesmeBedeli) if project.sozlesmeBedeli else  '-' ))
    # c.drawString(50, 390, "Sözleşme bedeli kdv dahil:%s" % ("{:,}".format(project.sozlesmeBedeliKdv) if project.sozlesmeBedeliKdv else  '-' ))
    #
    #

    # c.setFont("Verdana", 15)
    # c.drawString(50,440,'Hakediş Bilgileri')
    # c.line(50, 430, 200, 430)
    c.setFont("Verdana", 12)

    if text and text is not None:
        c.drawString(300, 150, 'Sayın %s:'%text)
        c.drawString(300,130,'Bilgilerinize arz olunur.')
    # else:
        # c.drawString(300, 150, 'Sayın:.............')
        # c.drawString(300, 130, 'Bilgilerinize arz olunur.')







    c.showPage()

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


# --------------------------------------------



@login_required
def edit_project_pdf_teknik(request,pk):
    project = EPProject.objects.get(pk=pk)
    text=""
    text=request.GET.get('get')


    days = None
    if project.aifinish:
        days = (project.aifinish - timezone.now()).days


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ProjeTakip.pdf"'
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.setTitle('Kobiltek Bilişim')

    logo = ImageReader('http://kobiltek.com:81/etutproje/'+MEDIA_URL + "profile/logo.png")
    c.drawImage(logo, 460, 740, width=80, height=80, mask='auto')
    # for i in range(5):
    #     page_num = c.getPageNumber()
    #     # text = "Proje Takip Programi %s" % page_num

    # data = "ğçİöşü"
    # p = Paragraph(data.decode('utf-8'), style=styNormal)

    # c.setFont("Times-Roman", 32)





    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))

    c.setFont("Verdana", 8)

    c.drawString(50, 800, " Rapor Tarih:" )

    c.drawString(105, 800, "%s" % datetime.datetime.today().strftime('%d-%m-%Y %H:%M'))




    c.setFont("Verdana", 16)
    c.drawString(100,770,'DESTEK HİZMETLERİ DAİRE BAŞKANLIĞI ')
    c.drawString(120, 745, ' ETÜT PROJE ŞUBE MÜDÜRLÜĞÜ')






    c.setFont("Verdana", 15)
    name=''
    count=1
    control=True
    kelime=''
    for item  in project.name:
        kelime+=item

        if count==58:
            c.drawString(50, 720, "%s" % name)
            name = ''
        elif count==116:
            c.drawString(50, 700, "%s" % name)
            name = ''
            control=False

        if item ==' ':
            name+=' '
            name+=kelime
            kelime=''


        if len(project.name)==count:
            name+=' '
            name+=kelime
        count=count+1
    if control:
        name
        c.drawString(50, 700, "%s" % name)
    else:
        c.drawString(50, 680, "%s" % name)




    # c.line(50, 720, 550, 720)

    c.setFont("Verdana", 15)
    c.drawString(50,650,'Genel Bilgiler')
    c.line(50, 640, 470, 640)



    c.setFont("Verdana", 10)
    c.drawString(50,620,"İl                       :%s" %project.city)
    if project.town:
        c.drawString(50,600,"İlçe                    :%s" %project.town)
    else:
        c.drawString(50, 600, "İlçe                    :%s" % project.town)
    c.drawString(50,580,"Yatırım Programı :%s" %project.butceCinsi)
    c.drawString(50,560,"Bütçe Yılı            :%s" %project.butceYili)
    # c.drawString(50, 540, "Projenin Aşaması :%s" % project.phases.all().order_by(
    #     'phaseDate').last() if project.phases.all().order_by('phaseDate').last() else ' ')



    c.drawString(300,620,"Projenin Cinsi          :%s" %project.projeCinsi)
    c.drawString(300,600,"Karakteristik           :%s" %project.karakteristik)
    c.drawString(300,580,"Projenin Durumu     :%s" %project.projectStatus)

    if project.sorumlu:
        c.drawString(300,560,"Projenin Sorumlusu :%s" %project.sorumlu  )
    else:
        c.drawString(300, 560, "Projenin Sorumlusu:")

    y = 540
    if project.offers.all():
        c.setFont("Verdana", 15)
        c.drawString(300, y, 'Görüş ve Öneriler:')
        y -= 10
        c.line(300, y, 450, y)
        c.setFont("Verdana", 10)

        # c.setFillColorRGB(0, 0, 0.77)
        #   y440
        y -= 20
        c.drawString(300, y, 'İsim-Soyisim')
        c.line(300, y - 10, 350, y - 10)

        c.drawString(400, y, 'Görüş ')
        c.line(400, y - 10, 450, y - 10)
        y -= 20
        for item in project.offers.all().order_by('creationDate')[:3]:
            if y > 150:
                c.drawString(300, y, '%s' % item.added_by)
                c.drawString(400, y, '%s' % item.message)
                y -= 20
            else:
                page_num = c.getPageNumber()
                c.showPage()
                pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
                # c.drawString(50, 25, 'http:/www.kobiltek.com/')
                # c.drawString(450, 25, 'Proje Takip Sistemi')
                page_num = c.getPageNumber()
                # c.drawString(280, 25, '%s' % page_num)
                y = 750

        page_num = c.getPageNumber()




    # c.setFont("Verdana", 15)
    # c.drawString(50,590,'İhale Bilgileri')
    # c.line(50, 580, 200, 580)
    # c.setFont("Verdana", 10)
    #
    # c.drawString(50, 560, "İhale Tarihi                         :%s" % (project.ihaleTarihi.strftime('%m/%d/%Y') if project.ihaleTarihi else  ' '))
    # c.drawString(50, 540, "Sözleşme Tarihi                  :%s" %(project.sozlesmeTarihi.strftime('%m/%d/%Y')  if project.sozlesmeTarihi else  ' ' ))
    # c.drawString(50, 520, "Alım İşinin Başlangıç Tarihi  :%s" %(project.aistart.strftime('%m/%d/%Y')  if project.aistart else  ' ' ))
    # c.drawString(50, 500, "Alım İşinin Bitiş Tarihi         :%s"%(project.aifinish.strftime('%m/%d/%Y')  if project.aifinish else  ' ' ))
    # c.drawString(50, 480, "İşin Süresi                         :%s (Gün)" % (project.isSUresi if project.isSUresi else  ' ' ))
    #
    #
    # c.drawString(50, 460, "Kaç Gün Kaldi                    :%s (Gün)" % (days if  days else  ' ' ))

    if project.employees.all():
        c.setFont("Verdana", 15)
        c.drawString(50, 520, 'Personel Listesi:')
        c.line(50, 510, 200, 510)
        c.setFont("Verdana", 10)

        # c.setFillColorRGB(0, 0, 0.77)

        c.drawString(50, 490, 'İsim-Soyisim')
        c.line(50, 480, 150, 480)

        c.drawString(200, 490, 'Kontrol Alanı')
        c.line(200, 480, 250, 480)

        y = 470

        for item in project.employees.all():

            if y > 150:
                c.drawString(50, y, '%s' % item.employee)
                c.drawString(200, y, '%s' % item.projectEmployeeTitle)
                y -= 20
            else:
                page_num = c.getPageNumber()
                c.showPage()
                pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
                # c.drawString(50, 25, 'http:/www.kobiltek.com/')
                # c.drawString(450, 25, 'Proje Takip Sistemi')
                page_num = c.getPageNumber()
                # c.drawString(280, 25, '%s' % page_num)
                y = 750


        page_num = c.getPageNumber()
        #
        # c.drawString(50, 25, 'http:/www.kobiltek.com/')
        c.drawString(280, 25, '%s' % page_num)
        # c.drawString(450, 25, 'Proje Takip Sistemi')




    c.setFont("Verdana", 12)

    if text and text is not None:
        c.drawString(300, 150, 'Sayın %s:'%text)
        c.drawString(300,130,'Bilgilerinize arz olunur.')
    # else:
        # c.drawString(300, 150, 'Sayın:.............')
        # c.drawString(300, 130, 'Bilgilerinize arz olunur.')


    c.showPage()

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response