from django.contrib.auth import logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from wushu.Forms.CategoryItemForm import CategoryItemForm
from wushu.Forms.CommunicationForm import CommunicationForm
from wushu.Forms.DisabledCommunicationForm import DisabledCommunicationForm
from wushu.Forms.DisabledPersonForm import DisabledPersonForm
from wushu.Forms.DisabledUserForm import DisabledUserForm
from wushu.Forms.UserForm import UserForm
from wushu.Forms.PersonForm import PersonForm
from wushu.Forms.UserSearchForm import UserSearchForm
from wushu.models import Judge, CategoryItem, Person, Communication
from wushu.services import general_methods


@login_required
def return_add_referee(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = UserForm()
    person_form = PersonForm()
    communication_form = CommunicationForm()

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST, request.FILES)
        communication_form = CommunicationForm(request.POST)

        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid():
            user = User()
            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            group = Group.objects.get(name='Hakem')
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            user.groups.add(group)
            user.save()

            person = person_form.save(commit=False)
            communication = communication_form.save(commit=False)
            person.save()
            communication.save()

            judge = Judge(user=user, person=person, communication=communication)

            judge.save()

            subject, from_email, to = 'WUSHU - Hakem Bilgi Sistemi Kullanıcı Giriş Bilgileri', 'no-reply@twf.gov.tr:81', user.email
            text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            html_content = '<p> <strong>Site adresi: </strong> <a href="http://sbs.twf.gov.tr:81/"></a>sbs.twf.gov.tr<</p>'
            html_content = html_content + '<p><strong>Kullanıcı Adı:  </strong>' + user.username + '</p>'
            html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, 'Hakem Başarıyla Kayıt Edilmiştir.')

            return redirect('wushu:hakemler')

        else:

            for x in user_form.errors.as_data():
                messages.warning(request, user_form.errors[x][0])

    return render(request, 'hakem/hakem-ekle.html',
                  {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form})


@login_required
def return_referees(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    referees = Judge.objects.all()
    user_form = UserSearchForm()
    if request.method == 'POST':
        user_form = UserSearchForm(request.POST)
        if user_form.is_valid():
            firstName = user_form.cleaned_data.get('first_name')
            lastName = user_form.cleaned_data.get('last_name')
            email = user_form.cleaned_data.get('email')
            if not (firstName or lastName or email):
                messages.warning(request, 'Lütfen Arama Kriteri Giriniz.')
            else:
                query = Q()
                if lastName:
                    query &= Q(user__last_name__icontains=lastName)
                if firstName:
                    query &= Q(user__first_name__icontains=firstName)
                if email:
                    query &= Q(user__email__icontains=email)
                referees = Judge.objects.filter(query)
    return render(request, 'hakem/hakemler.html', {'referees': referees, 'user_form': user_form})


@login_required
def return_level(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    category_item_form = CategoryItemForm();

    if request.method == 'POST':

        category_item_form = CategoryItemForm(request.POST)

        if category_item_form.is_valid():

            categoryItem = CategoryItem(name=category_item_form.cleaned_data['name'])
            categoryItem.forWhichClazz = "VISA"
            categoryItem.save()

            return redirect('wushu:seviye')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')
    categoryitem = CategoryItem.objects.filter(forWhichClazz="VISA")
    return render(request, 'hakem/seviye.html',
                  {'category_item_form': category_item_form, 'categoryitem': categoryitem})


@login_required
def categoryItemDelete(request, pk):
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
def categoryItemUpdate(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    categoryItem = CategoryItem.objects.get(id=pk)
    category_item_form = CategoryItemForm(request.POST or None, instance=categoryItem)
    if request.method == 'POST':
        if category_item_form.is_valid():
            category_item_form.save()
            messages.success(request, 'Başarıyla Güncellendi')
            return redirect('wushu:seviye')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'hakem/seviyeDuzenle.html',
                  {'category_item_form': category_item_form})


@login_required
def deleteReferee(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Judge.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Judge.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def updateReferee(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    judge = Judge.objects.get(pk=pk)
    user = User.objects.get(pk=judge.user.pk)
    person = Person.objects.get(pk=judge.person.pk)
    communication = Communication.objects.get(pk=judge.communication.pk)
    user_form = UserForm(request.POST or None, instance=user)
    person_form = PersonForm(request.POST or None, instance=person)
    communication_form = CommunicationForm(request.POST or None, instance=communication)
    if request.method == 'POST':
        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid():

            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.save()
            person_form.save()
            communication_form.save()

            messages.success(request, 'Hakem Başarıyla Güncellendi')
            return redirect('wushu:hakemler')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'hakem/hakemDuzenle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form})


@login_required
def updateRefereeProfile(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user = request.user
    referee_user = Judge.objects.get(user=user)
    person = Person.objects.get(pk=referee_user.person.pk)
    communication = Communication.objects.get(pk=referee_user.communication.pk)
    user_form = DisabledUserForm(request.POST or None, instance=user)
    person_form = DisabledPersonForm(request.POST or None, request.FILES or None, instance=person)
    communication_form = DisabledCommunicationForm(request.POST or None, instance=communication)
    password_form = SetPasswordForm(request.user, request.POST)

    if request.method == 'POST':
        data = request.POST.copy()
        data['bloodType'] = "AB Rh+"
        data['gender'] = "Erkek"
        person_form = DisabledPersonForm(data)

        if person_form.is_valid() and password_form.is_valid():
            if len(request.FILES)>0:
                person.profileImage = request.FILES['profileImage']
                person.save()
                messages.success(request, 'Profil Fotoğrafı Başarıyla Güncellenmiştir.')

            user.set_password(password_form.cleaned_data['new_password2'])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifre Başarıyla Güncellenmiştir.')
            return redirect('wushu:hakem-profil-guncelle')



        elif person_form.is_valid() and not password_form.is_valid():
            if len(request.FILES)>0:
                person.profileImage = request.FILES['profileImage']
                person.save()
                messages.success(request, 'Profil Fotoğrafı Başarıyla Güncellenmiştir.')
            else:
                messages.warning(request, 'Alanları Kontrol Ediniz')
            return redirect('wushu:hakem-profil-guncelle')


        elif not person_form.is_valid() and password_form.is_valid():
            user.set_password(password_form.cleaned_data['new_password2'])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifre Başarıyla Güncellenmiştir.')
            return redirect('wushu:hakem-profil-guncelle')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz.')

            return redirect('wushu:hakem-profil-guncelle')

    return render(request, 'hakem/hakem-profil-guncelle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'password_form': password_form})
