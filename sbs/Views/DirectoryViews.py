from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from sbs.Forms.CommunicationForm import CommunicationForm
from sbs.Forms.DirectoryCommissionForm import DirectoryCommissionForm
from sbs.Forms.DirectoryForm import DirectoryForm
from sbs.Forms.DirectoryMemberRoleForm import DirectoryMemberRoleForm
from sbs.Forms.DisabledCommunicationForm import DisabledCommunicationForm
from sbs.Forms.DisabledDirectoryForm import DisabledDirectoryForm
from sbs.Forms.DisabledPersonForm import DisabledPersonForm
from sbs.Forms.DisabledSportClubUserForm import DisabledSportClubUserForm
from sbs.Forms.DisabledUserForm import DisabledUserForm
from sbs.Forms.UserForm import UserForm
from sbs.Forms.PersonForm import PersonForm
from sbs.Forms.UserSearchForm import UserSearchForm
from sbs.models import Person, Communication
from sbs.models.DirectoryCommission import DirectoryCommission
from sbs.models.DirectoryMember import DirectoryMember
from sbs.models.DirectoryMemberRole import DirectoryMemberRole
from sbs.services import general_methods


@login_required
def add_directory_member(request):
    perm =general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = UserForm()
    person_form = PersonForm()
    communication_form = CommunicationForm()
    member_form = DirectoryForm()

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST, request.FILES)
        communication_form = CommunicationForm(request.POST)
        member_form = DirectoryForm(request.POST)

        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and member_form.is_valid():
            user = User()
            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            group = Group.objects.get(name='Yonetim')
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            user.groups.add(group)
            user.save()

            person = person_form.save(commit=False)
            communication = communication_form.save(commit=False)
            person.save()
            communication.save()

            directoryMember = DirectoryMember(user=user, person=person, communication=communication)
            directoryMember.role = member_form.cleaned_data['role']
            directoryMember.commission = member_form.cleaned_data['commission']

            directoryMember.save()

            subject, from_email, to = 'Halter - Yönetim/Federasyon Bilgi Sistemi Kullanıcı Giriş Bilgileri', 'no-reply@twf.gov.tr', user.email
            text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            html_content = '<p> <strong>Site adresi: </strong> <a href="http://sbs.twf.gov.tr:81/"></a>sbs.twf.gov.tr:81</p>'
            html_content = html_content + '<p><strong>Kullanıcı Adı:  </strong>' + user.username + '</p>'
            html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, 'Yönetim Kurulu Üyesi Başarıyla Kayıt Edilmiştir.')

            return redirect('sbs:kurul-uyeleri')

        else:

            for x in user_form.errors.as_data():
                messages.warning(request, user_form.errors[x][0])

    return render(request, 'yonetim/kurul-uyesi-ekle.html',
                  {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form, 'member_form':member_form})


@login_required
def return_directory_members(request):
    perm =general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    members = DirectoryMember.objects.all()
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
                members = DirectoryMember.objects.filter(query)
    return render(request, 'yonetim/kurul-uyeleri.html', {'members': members, 'user_form': user_form})


@login_required
def delete_directory_member(request, pk):
    perm =general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = DirectoryMember.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except DirectoryMember.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def update_directory_member(request, pk):
    perm =general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    member = DirectoryMember.objects.get(pk=pk)
    user = User.objects.get(pk=member.user.pk)
    person = Person.objects.get(pk=member.person.pk)
    communication = Communication.objects.get(pk=member.communication.pk)
    user_form = UserForm(request.POST or None, instance=user)
    person_form = PersonForm(request.POST or None, instance=person)
    communication_form = CommunicationForm(request.POST or None, instance=communication)
    member_form = DirectoryForm(request.POST or None, instance=member)
    if request.method == 'POST':
        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and member_form.is_valid():

            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.save()
            person_form.save()
            communication_form.save()
            member_form.save()

            messages.success(request, 'Yönetim Kurulu Üyesi Başarıyla Güncellendi')
            return redirect('sbs:kurul-uyeleri')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'yonetim/kurul-uyesi-duzenle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'member_form':member_form})


@login_required
def return_member_roles(request):
    perm =general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    member_role_form = DirectoryMemberRoleForm();

    if request.method == 'POST':

        member_role_form = DirectoryMemberRoleForm(request.POST)

        if member_role_form.is_valid():

            memberRole = DirectoryMemberRole(name=member_role_form.cleaned_data['name'])
            memberRole.save()
            messages.success(request, 'Kurul Üye Rolü Başarıyla Kayıt Edilmiştir.')
            return redirect('sbs:kurul-uye-rolleri')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')
    memberRoles = DirectoryMemberRole.objects.all()
    return render(request, 'yonetim/kurul-uye-rolleri.html',
                  {'member_role_form': member_role_form, 'memberRoles': memberRoles})


@login_required
def delete_member_role(request, pk):
    perm =general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = DirectoryMemberRole.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except DirectoryMemberRole.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def update_member_role(request, pk):
    perm =general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    memberRole = DirectoryMemberRole.objects.get(id=pk)
    member_role_form = DirectoryMemberRoleForm(request.POST or None, instance=memberRole)

    if request.method == 'POST':
        if member_role_form.is_valid():
            member_role_form.save()
            messages.success(request, 'Başarıyla Güncellendi')
            return redirect('sbs:kurul-uye-rolleri')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'yonetim/kurul-uye-rol-duzenle.html',
                  {'member_role_form': member_role_form})


@login_required
def return_commissions(request):
    perm =general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    commission_form = DirectoryCommissionForm()

    if request.method == 'POST':

        commission_form = DirectoryCommissionForm(request.POST)

        if commission_form.is_valid():

            commission = DirectoryCommission(name=commission_form.cleaned_data['name'])
            commission.save()
            messages.success(request, 'Kurul Başarıyla Kayıt Edilmiştir.')
            return redirect('sbs:kurullar')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')
    commissions = DirectoryCommission.objects.all()
    return render(request, 'yonetim/kurullar.html',
                  {'commission_form': commission_form, 'commissions': commissions})


@login_required
def delete_commission(request, pk):
    perm =general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = DirectoryCommission.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except DirectoryCommission.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def update_commission(request, pk):
    perm =general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    commission = DirectoryCommission.objects.get(id=pk)
    commission_form = DirectoryCommissionForm(request.POST or None, instance=commission)

    if request.method == 'POST':
        if commission_form.is_valid():
            commission_form.save()
            messages.success(request, 'Başarıyla Güncellendi')
            return redirect('sbs:kurullar')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'yonetim/kurul-duzenle.html',
                  {'commission_form': commission_form})



@login_required
def updateDirectoryProfile(request):
    perm =general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')


    user = request.user
    directory_user = DirectoryMember.objects.get(user=user)
    person = Person.objects.get(pk=directory_user.person.pk)
    communication = Communication.objects.get(pk=directory_user.communication.pk)
    user_form = DisabledUserForm(request.POST or None, instance=user)
    person_form = DisabledPersonForm(request.POST or None, instance=person)
    communication_form = DisabledCommunicationForm(request.POST or None, instance=communication)
    member_form = DisabledDirectoryForm(request.POST or None, instance=directory_user)
    password_form = SetPasswordForm(request.user, request.POST)




    if request.method == 'POST':

        if user_form.is_valid() and communication_form.is_valid() and person_form.is_valid() and member_form.is_valid() and password_form.is_valid():

            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.set_password(password_form.cleaned_data['new_password1'])
            user.save()

            person_form.save()
            communication_form.save()
            member_form.save()
            password_form.save()

            messages.success(request, 'Yönetim Kurul Üyesi Başarıyla Güncellenmiştir.')

            return redirect('sbs:yonetim-kurul-profil-guncelle')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'yonetim/yonetim-kurul-profil-guncelle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'password_form': password_form, 'member_form': member_form})