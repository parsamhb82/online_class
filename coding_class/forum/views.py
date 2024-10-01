from django.shortcuts import render
from .serilizers import CreateRoomSerilizer, CreateMessageSerilizer, UpdateMessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Forum, Room, Message
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

class CreateRoomView(CreateAPIView):
    serializer_class = CreateRoomSerilizer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.userprofile not in self.request.data['forum'].online_class.teacher.all():
            raise Exception('You are not a teacher of this class')
        serializer.save(creator=self.request.user.userprofile)

class CreateMessageView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = CreateMessageSerilizer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user.userprofile)

class UpdateMessageView(UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = UpdateMessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user.userprofile != self.get_object().sender:
            raise Exception('You are not the sender of this message')
        serializer.save()

class DeleteMessageView(DestroyAPIView):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user.userprofile != instance.sender:
            raise Exception('You are not the sender of this message')
        return super().perform_destroy(instance)

class DeleteRoomView(DestroyAPIView):
    queryset = Room.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user.userprofile not in instance.forum.online_class.teacher.all():
            raise Exception('You dont have the access to remove this room')
        return super().perform_destroy(instance)