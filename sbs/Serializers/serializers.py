from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from sbs.models.Message import Message
from rest_framework.serializers import ModelSerializer, CharField
from django.http import JsonResponse
from rest_framework import serializers

from sbs.models.Employee import Employee
from sbs.models.Person import Person
from sbs.models.CategoryItem import CategoryItem
from sbs.models.Company import Company

class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            User, username=validated_data['recipient']['username'])
        msg = Message(recipient=recipient,
                      body=validated_data['body'],
                      user=user)

        if Message.objects.filter(user=recipient, recipient=user) or Message.objects.filter(user=user,
                                                                                            recipient=recipient):
            if Message.objects.filter(user=recipient, recipient=user):
                msg.chat_id = Message.objects.filter(user=recipient, recipient=user)[0].chat_id
            elif Message.objects.filter(user=user, recipient=recipient):
                msg.chat_id = Message.objects.filter(user=user, recipient=recipient)[0].chat_id

        msg.save()
        return msg

    class Meta:
        model = Message
        fields = ('id', 'user', 'recipient', 'creationDate', 'body')

class UserModelSerializer(ModelSerializer):
    image = serializers.SerializerMethodField('imageGet')

    def imageGet(self, user):
        # Kullanicilarin resimleri
        try:
            return str(Employee.objects.get(user__username=user).person.profileImage)
        except:
            # admin olma durumu
            return 'profile/logo.png'


    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'image']


class MessageEndModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    recipient = UserModelSerializer()

    class Meta:
        model = Message
        fields = '__all__'


class PersonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class CategoryItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryItem
        fields = '__all__'


class EmployeModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    person = PersonModelSerializer()
    workDefinition = CategoryItemModelSerializer()

    class Meta:
        model = Employee
        fields = '__all__'


class CompanyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
