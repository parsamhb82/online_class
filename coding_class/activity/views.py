from django.shortcuts import render
from .serilizers import ActivitySerializer
from .models import Activity
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, DestroyAPIView
from online_class.models import OnlineClass
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
class CreateActivityView(CreateAPIView):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        online_class = get_object_or_404(OnlineClass, id=self.request.data['online_class'])
        if self.request.user.userprofile not in online_class.teachers.all():
            raise PermissionDenied("You are not allowed to create activities for this class.")
        serializer.save()

class DestroyActivityView(DestroyAPIView):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user.userprofile not in instance.online_class.teachers.all():
            raise PermissionDenied("You are not allowed to delete activities for this class.")
        instance.delete()

