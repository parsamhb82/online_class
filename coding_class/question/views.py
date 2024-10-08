from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AssignmentSerilizer, CreateFileQuestionAnswerSerializer, CreateTextQuestionAnswerSerializer, CreateQuestionSerializer
from .models import Question, Assignment, Team
from rest_framework.permissions import IsAuthenticated
from online_class.models import OnlineClass
from .serializers import CreateTeamSerializer

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
        
class CreateQuestion(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateQuestionSerializer
    queryset = Question.objects.all()

    def perform_create(self, serializer):
        assignment_id = self.request.data.get('assignment')
        assignment = Assignment.objects.get(id=assignment_id)
        online_class = assignment.online_class
        user_profile = self.request.user.userprofile
        if user_profile not in online_class.teachers.all() or user_profile not in online_class.mentors.all():
            return Response({"message" : "you cant create a question"}, status= status.HTTP_403_FORBIDDEN)
        return super().perform_create(serializer)

class CreateTextQuestionAnswer(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateTextQuestionAnswerSerializer
    queryset = Question.objects.all()
    def perform_create(self, serializer):
        student = self.request.user.userprofile
        question = serializer.validated_data['question']
        if student not in question.assignment.online_class.students.all():
            return Response({"message" : "you cant answer this question"}, status= status.HTTP_403_FORBIDDEN)
        serializer.save(student=student)


class CreateFileQuestionAnswer(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateFileQuestionAnswerSerializer
    queryset = Question.objects.all()
    def perform_create(self, serializer):
        student = self.request.user.userprofile
        question = serializer.validated_data['question']
        if student not in question.assignment.online_class.students.all():
            return Response({"message" : "you cant answer this question"}, status= status.HTTP_403_FORBIDDEN)
        serializer.save(student=student)


class CreateTeamView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateTeamSerializer
    queryset = Team.objects.all()
    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        assignment = question.assignment
        online_class = assignment.online_class
        user_profile = self.request.user.userprofile
        if user_profile not in online_class.teachers.all() or user_profile not in online_class.mentors.all():
            return Response({"message" : "you cant create a team"}, status= status.HTTP_403_FORBIDDEN)
        return super().perform_create(serializer)


    
