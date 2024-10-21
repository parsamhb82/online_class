from django.shortcuts import render
from .serilizers import CreateOnlineClassSerilizer, UpdateOnlineClassSerilizer, OnlineClassViewStudetsView, AddUserToClassSerializer
from .models import OnlineClass
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from .permissions import IsTeacherOfClass
from  django.contrib.auth.models import User
from .serilizers import EnterTheClassByPasswordSerializer, StudentsClassViewSerializer, AddStudentToClassSerializer
from django.contrib.auth.hashers import make_password
import secrets
from .models import Enrollment
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.http import urlencode
from activity.models import StudentActivity
from django.db.models import Sum

def generate_token():
    return secrets.token_urlsafe(16)


class CreateOnlineClass(CreateAPIView):
    queryset = OnlineClass.objects.all()
    serializer_class = CreateOnlineClassSerilizer
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {'request': self.request}
        return super().get_serializer(*args, **kwargs)

class UpdateOnlineClass(UpdateAPIView):
    queryset = OnlineClass.objects.all()
    serializer_class = UpdateOnlineClassSerilizer
    permission_classes = [IsAuthenticated, IsTeacherOfClass]

    # only patch method is allowed
    http_method_names = ['patch']

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {'request': self.request}
        return super().get_serializer(*args, **kwargs)

class OnlineClassViewStudetsView(RetrieveAPIView):
    queryset = OnlineClass.objects.all()
    serializer_class = OnlineClassViewStudetsView
    permission_classes = [IsAuthenticated, IsTeacherOfClass]

class AddMentorToClass(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOfClass]

    def post(self, request, *args, **kwargs):
        serializer = AddUserToClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            online_class_code = serializer.validated_data['code']
            mentors_username = serializer.validated_data['username']
            mentor = User.objects.get(username=mentors_username).userprofile
            online_class = OnlineClass.objects.get(code=online_class_code)
            online_class.mentors.add(mentor)
            online_class.save()
            return Response({'message': 'Mentor added successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Mentor not found'}, status=status.HTTP_404_NOT_FOUND)
        except OnlineClass.DoesNotExist:
            return Response({'message': 'Online class not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AddTeacherToClass(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOfClass]

    def post(self, request, *args, **kwargs):
        serializer = AddUserToClassSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        try:
            online_class_code = serializer.validated_data['code']
            teachers_username = serializer.validated_data['username']
            teacher = User.objects.get(username=teachers_username).userprofile
            online_class = OnlineClass.objects.get(code=online_class_code)
            online_class.teachers.add(teacher)
            online_class.save()
            return Response({'message': 'teacher added successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        except OnlineClass.DoesNotExist:
            return Response({'message': 'Online class not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RemoveStudentFromClass(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOfClass]

    def post(self, request, *args, **kwargs):
        serializer = AddUserToClassSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        try:
            online_class_code = serializer.validated_data['code']
            students_username = serializer.validated_data['username']
            student = User.objects.get(username=students_username).userprofile
            online_class = OnlineClass.objects.get(code=online_class_code)
            if student not in online_class.students.all():
                return Response({"message" : "student not found in this class"}, status=status.HTTP_421_MISDIRECTED_REQUEST)
            online_class.students.remove(student)
            online_class.save()
        except User.DoesNotExist:
            return Response({'message': 'student not found'}, status=status.HTTP_404_NOT_FOUND)
        except OnlineClass.DoesNotExist:
            return Response({'message': 'Online class not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class EnterTheClassByPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = EnterTheClassByPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            userprofile = request.user.userprofile
            online_class_code = serializer.validated_data['code']
            password = serializer.validated_data['password']
            password = make_password(password)
            online_class = OnlineClass.objects.get(code=online_class_code)
            if userprofile in online_class.students.all() or userprofile in online_class.mentors.all() or userprofile in online_class.teachers.all():
                return Response({'message': 'You are already a member of this class'}, status=status.HTTP_400_BAD_REQUEST)
            if online_class.password != password:
                return Response({'message': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
            online_class.students.add(userprofile)
            return Response({'message': 'Password is correct and you are added to the class'}, status=status.HTTP_200_OK)
        except OnlineClass.DoesNotExist:    
            return Response({'message': 'Online class not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class SendInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AddUserToClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            online_class = OnlineClass.objects.get(code=serializer.validated_data['code'])
            user = User.objects.get(username=serializer.validated_data['username'])
            userprofile = user.userprofile
            if userprofile in online_class.students.all() or userprofile in online_class.mentors.all() or userprofile in online_class.teachers.all():
                return Response({'message': 'User is already a member of this class'}, status=status.HTTP_400_BAD_REQUEST)
            if online_class.password != None:
                return Response({'message': 'You cannot send an invite to this class because it has a password'}, status=status.HTTP_400_BAD_REQUEST)
            if not online_class.is_private:
                return Response({'message': 'You cannot send an invite to this class because it is public'}, status=status.HTTP_400_BAD_REQUEST)
            token = generate_token()
            enrollment = Enrollment.objects.create(userprofile=userprofile, online_class=online_class, token=token)
            confirmation_link = request.build_absolute_uri(reverse('confirm-enrollment')+ '?' + urlencode({'token': token}))
            send_mail(
                subject='Invitation to join the class',
                message=f"You have been invited to join the class {online_class.name} by {request.user.username}. Please click on the following link to confirm your enrollment: {confirmation_link}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            return Response({'message': 'Invitation sent successfully'}, status=status.HTTP_200_OK)
        except OnlineClass.DoesNotExist:
            return Response({'message': 'Online class not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ConfirmEnrollmentView(APIView):
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'error': 'Invalid token'}, status=400)
        
        enrollment = get_object_or_404(Enrollment, token=token)
        if enrollment.is_active:
           return Response({'error': 'Enrollment already confirmed'}, status=400)
        enrollment.is_active = True
        enrollment.token = None
        enrollment.class_enrolled.students.add(enrollment.userprofile)
        enrollment.class_enrolled.save()#dunno if it works fine
        enrollment.save()
        return Response({'message': 'Enrollment confirmed successfully'}, status=200)

class StudentClassView(ListAPIView):
    queryset = OnlineClass.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = StudentsClassViewSerializer

    def get_queryset(self):
        return OnlineClass.objects.filter(available=True)

class StudentAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddStudentToClassSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        try:
            class_code = serializer.validated_data['code']
            online_class = OnlineClass.objects.get(code=class_code)
            user = request.user
            student = user.userprofile
            if student in online_class.students.all() and student in online_class.mentors.all() and student in online_class.teachers.all():
                return Response({'message': 'User is already a member of this class'}, status=status.HTTP_400_BAD_REQUEST)
            if online_class.is_private == True:
                return Response({'message': 'You cannot add a student to this class because it is private'}, status=status.HTTP_400_BAD_REQUEST)
            if online_class.has_limit and online_class.students.count() >= online_class.limit:
                online_class.available = False
                return Response({'message': 'You cannot add a student to this class because it has reached its limit'}, status=status.HTTP_400_BAD_REQUEST)
            online_class.students.add(student)
            online_class.save()
            return Response({'message': 'Student added successfully'}, status=status.HTTP_200_OK)
        except OnlineClass.DoesNotExist:
            return Response({'message': 'Online class not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class StudentsScoreSheet(APIView):##needs to be tested
    permission_classes = [IsAuthenticated]
    def get(self, request, class_code):
        try:
            online_class = OnlineClass.objects.get(code=class_code)
            user = request.user
            user_profile = user.userprofile
            if online_class.is_private == True and user_profile not in online_class.students.all() and user_profile not in online_class.mentors.all() and user_profile not in online_class.teachers.all():
                return Response({'message': 'You cannot view the score sheet of this class because it is private'}, status=status.HTTP_400_BAD_REQUEST)
            
            student_activities = StudentActivity.objects.filter(activity__online_class=online_class)
            students_scores = student_activities.values('userprofile__user__username').annotate(total_score=Sum('score')).order_by('-total_score')
            
            # Format the scoresheet as a list of dictionaries
            scoresheet = [
                {'username': student['userprofile__user__username'], 'total_score': student['total_score']}
                for student in students_scores
            ]
            
            # Return the scoresheet in the response
            return Response({'scoresheet': scoresheet}, status=status.HTTP_200_OK)
        

        except OnlineClass.DoesNotExist:
            return Response({'message': 'Online class not found'}, status=status.HTTP_404_NOT_FOUND)

            
    












    
