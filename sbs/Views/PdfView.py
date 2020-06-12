

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
from sbs.models.Town import Town
from sbs.models.Employee import Employee

from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak




# excel
import csv
import xlwt

@login_required

def html_to_pdf_view(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')


    buffer = BytesIO()
    c = canvas.Canvas(buffer)
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
        c.setFont("Times-Roman", 32)
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

    kalan=102
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ProjeTakip.pdf"'
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.setTitle('Kobiltek Bilişim')
    # for i in range(5):
    #     page_num = c.getPageNumber()
    #     # text = "Proje Takip Programi %s" % page_num

    # data = "ğçİöşü"
    # p = Paragraph(data.decode('utf-8'), style=styNormal)

    # c.setFont("Times-Roman", 32)

    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    c.setFont("Verdana", 32)
    # text = "Proje Takip Programi "
    # c.drawString(150, 750, text)

    c.drawString(50,750,"%s" %project.name)
    c.line(50, 740, 550, 740)
    c.setFont("Verdana", 10)
    c.drawString(50,680,"İl                       :%s" %project.city)
    if project.town:
        c.drawString(50,660,"İlçe                    :%s" %project.town)
    else:
        c.drawString(50, 660, "İlçe                    :%s" % project.town)
    c.drawString(50,640,"Yatırım Programı :%s" %project.butceCinsi)
    c.drawString(50,620,"Bütçe yılı            :%s" %project.butceYili)
    c.drawString(300,680,"Projenin Cinci          :%s" %project.projeCinsi)
    c.drawString(300,660,"Karakteristik           :%s" %project.karakteristik)
    c.drawString(300,640,"Projenin Durumu     :%s" %project.projectStatus)

    if project.sorumlu:
        c.drawString(300,620,"Projenin Sorumlusu :%s" %project.sorumlu  )
    else:
        c.drawString(300, 620, "Projenin Sorumlusu:")


    c.setFont("Verdana", 20)
    c.drawString(50,590,'İhale Bilgileri')
    c.line(50, 580, 200, 580)
    c.setFont("Verdana", 10)

    c.drawString(50, 560, "İhale tarihi                         :%s" % (project.ihaleTarihi.strftime('%m/%d/%Y') if project.ihaleTarihi else  '-'))
    c.drawString(50, 540, "Sözleşme tarihi                  :%s" %(project.sozlesmeTarihi.strftime('%m/%d/%Y')  if project.sozlesmeTarihi else  '-' ))
    c.drawString(50, 520, "Alım İşinin Başlangıç tarihi  :%s" %(project.aistart.strftime('%m/%d/%Y')  if project.aistart else  '-' ))
    c.drawString(50, 500, "Alım İşinin Bitiş tarihi         :%s"%(project.aifinish.strftime('%m/%d/%Y')  if project.aifinish else  '-' ))
    c.drawString(50, 480, "İşin Süresi                         :%s" % (project.isSUresi if project.isSUresi else  '-' ))
    c.drawString(50, 460, "Kaç Gün kaldi                    :%s" % (kalan if kalan else  '-' ))
    c.setFont("Verdana", 20)
    c.drawString(300,590,'Arsa Yapım Ödenek Bilgileri')
    c.line(300, 580, 450, 580)
    c.setFont("Verdana", 10)
    c.drawString(300, 560, "Arsa Alanı                   :%s" % (project.arsaAlani if project.arsaAlani else  '-' ))
    c.drawString(300, 540, "İnşaat alanı                 :%s" % (project.insaatAlani if project.insaatAlani else  '-' ))
    c.drawString(300, 520, "Tahmini Ödenek Tutari:%s" % (project.tahminiOdenekTutari if project.tahminiOdenekTutari else  '-' ))
    c.drawString(300, 500, "Yaklaşık Maliyet          :%s" % (project.yaklasikMaliyet if project.yaklasikMaliyet else  '-' ))






    c.setFont("Verdana", 20)
    c.drawString(300,470,'Hakediş Bilgileri')
    c.line(300, 460, 450, 460)
    c.setFont("Verdana", 10)
    c.drawString(300, 440, "Sözleşme bedeli               :%s" % (project.sozlesmeBedeli if project.sozlesmeBedeli else  '-' ))
    c.drawString(300, 420, "Sözleşme bedeli kdv dahil:%s" % (project.sozlesmeBedeliKdv if project.sozlesmeBedeliKdv else  '-' ))



    c.setFont("Verdana", 20)
    c.drawString(50,390,'Personel Listesi ')
    c.line(50, 380, 200, 380)
    c.setFont("Verdana", 10)
    y=360
    for item in project.employees.all():
        print(item.employee)
        if y>0:
            c.drawString(50, y, '%s'%item.employee)
            y-=20
        else:
            page_num = c.getPageNumber()
            y=750

    c.setFont("Verdana", 20)
    c.drawString(300,390,'İhtiyaç Listesi ')
    c.line(300, 380, 450, 380)
    c.setFont("Verdana", 10)
    y=360
    for item in project.requirements.all():
        print(item.definition)
        if y>0:
            c.drawString(300, y, '%s'%item.definition)
            y-=20
        else:
            page_num = c.getPageNumber()
            y=750

    c.showPage()

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response




@login_required
def edit_project_excel(request,pk):

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

