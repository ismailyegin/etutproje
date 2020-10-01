from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework.response import Response
from sbs.models.Message import Message
from django.db.models import Q

from sbs.models.Message import Message
from sbs.models.Employee import Employee
from sbs.models.Company import Company

from sbs.Serializers.serializers import MessageModelSerializer, MessageEndModelSerializer, EmployeModelSerializer, \
    CompanyModelSerializer
from sbs.Serializers.serializers import UserModelSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from datetime import date, datetime
from django.shortcuts import get_object_or_404

import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


# from rest_framework.views import APIView


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """
    page_size = 20


class UserPagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """
    page_size = 50

class MessageModelViewSet(ModelViewSet):
    queryset = Message.objects.all().order_by("-creationDate")
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(Q(recipient=request.user) |
                                             Q(user=request.user))
        target = self.request.query_params.get('target', None)
        if target is not None:

            try:
                for message in Message.objects.filter(user__username=target, recipient=request.user):
                    message.is_show = True;
                    message.save()

                self.queryset = self.queryset.filter(
                    Q(recipient=request.user, user__username=target) |
                    Q(recipient__username=target, user=request.user))



            except:
                print('Ex ')

        return super(MessageModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(Q(recipient=request.user) |
                                 Q(user=request.user),
                                 Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        print('retrieve')
        return Response(serializer.data)


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = UserPagination  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)


class UserModelEndMessageViewSet(ModelViewSet):
    queryset = Message.objects.none()
    serializer_class = MessageEndModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        query = 'select * from (SELECT * FROM etutproje.sbs_message where user_id=%s or recipient_id=%s order by creationDate desc limit 10000) as t group by chat_id' % (
        request.user.pk, request.user.pk)
        messages = Message.objects.raw(query)
        for item in messages:
            self.queryset |= Message.objects.filter(pk=item.pk)

        return super(UserModelEndMessageViewSet, self).list(request, *args, **kwargs)

# class TestList(APIView):
#     authentication_classes = (CsrfExemptSessionAuthentication)
#     def get(self,request):
#         return Response({"message": "Hello, world!"})


class EmployeModelViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeModelSerializer

    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'user__email']


    # pagination_class = UserPagination  # Get all user

    def list(self, request, *args, **kwargs):
        return super(EmployeModelViewSet, self).list(request, *args, **kwargs)


class CompanyModelViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    # pagination_class = UserPagination  # Get all user

    def list(self, request, *args, **kwargs):
        return super(CompanyModelViewSet, self).list(request, *args, **kwargs)
