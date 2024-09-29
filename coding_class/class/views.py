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





    
