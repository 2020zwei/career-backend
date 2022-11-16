from django.shortcuts import render
from rest_framework.views import APIView
from .utils import login_user

class UserLoginView(APIView):

    def post(self, request, format=None):
        return login_user(request)