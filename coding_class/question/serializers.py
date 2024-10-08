from rest_framework import serializers
from .models import Assignment, Question, Team

class AssignmentSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = "__all__"