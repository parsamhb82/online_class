from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AssignmentSerilizer
from .models import Question, Assignment, Team
from rest_framework.permissions import IsAuthenticated
from online_class.models import OnlineClass

class CreateAssignment(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AssignmentSerilizer
    queryset = Assignment.objects.all()
    
    def perform_create(self, serializer):

        online_class = self.request.data.get('online_class')#need to be checked
        user_profile = self.request.user.userprofile
        if  user_profile not in online_class.teachers.all() or user_profile not in online_class.mentors.all():
            return Response({"message" : "you cant create an assignment"}, status= status.HTTP_403_FORBIDDEN)
        return super().perform_create(serializer)
    
class ShowAssignments(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AssignmentSerilizer
    queryset = Assignment.objects.all()

    def get_queryset(self):
        online_class_id = self.request.query_params.get('online_class_id')
        if online_class_id:
            try:
                online_class =  OnlineClass.objects.get(id=online_class_id)
            except OnlineClass.DoesNotExist:
                return Response({"message" : "online class not found"}, status= status.HTTP_404_NOT_FOUND)
            user_profile = self.request.user.userprofile
            if user_profile not in online_class.teachers.all() or user_profile not in online_class.mentors.all() or user_profile not in  online_class.students.all():
                return Response({"message" : "you cant view assignments"}, status= status.HTTP_403_FORBIDDEN)
            return Assignment.objects.filter(online_class=online_class)
        return Assignment.objects.none()
        


    
