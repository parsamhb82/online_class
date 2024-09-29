from django.shortcuts import render
from .serilizers import CreateOnlineClassSerilizer
from .models import OnlineClass
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView


class CreateOnlineClass(CreateAPIView):
    queryset = OnlineClass.objects.all()
    serializer_class = CreateOnlineClassSerilizer
    permission_classes = [IsAuthenticated]
