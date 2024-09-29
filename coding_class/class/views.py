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

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {'request': self.request}
        return super().get_serializer(*args, **kwargs)

class UpdateOnlineClass(UpdateAPIView):
    queryset = OnlineClass.objects.all()
    serializer_class = CreateOnlineClassSerilizer
    permission_classes = [IsAuthenticated]

    # only patch method is allowed
    http_method_names = ['patch']
    
