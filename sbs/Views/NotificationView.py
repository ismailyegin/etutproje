from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from sbs.services import general_methods
from sbs.models.Notification import Notification



@login_required
def notification(request):
    perm = general_methods.control_access_personel(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    notification=Notification.objects.filter(users=request.user).order_by('-creationDate').distinct()
    return render(request, 'notification/notification.html',
                  {
                      'notification': notification,
                   })