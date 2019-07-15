from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import CreateUserSerializer


class UsernameView(APIView):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count,
        }
        return Response(data)


class MobileView(APIView):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count,
        }

        return Response(data)


class UserView(CreateAPIView):
    serializer_class = CreateUserSerializer
