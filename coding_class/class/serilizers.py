from rest_framework import serializers
from .models import OnlineClass
import uuid
from django.contrib.auth.hashers import make_password

def generate_unique_class_code():
    while True:
        code = str(uuid.uuid4())[:32]
        if not OnlineClass.objects.filter(code=code).exists():
            return code

class CreateOnlineClassSerilizer(serializers.ModelSerializer):
    class Meta:
        model = OnlineClass
        fields = ['name', 'is_private', 'has_limit', 'limit', 'description', 'invitational', 'password', 'adding_start_time', 'adding_end_time']

    name = serializers.CharField(required=True)  #required
    is_private = serializers.BooleanField(required=False)  # Optional
    has_limit = serializers.BooleanField(required=False)  # Optional
    limit = serializers.IntegerField(required=False)  # Optional
    description = serializers.CharField(required=True)  # Optional
    invitational = serializers.BooleanField(required=False)  # Optional
    password = serializers.CharField(required=False)  # Optional
    adding_start_time = serializers.DateTimeField(required=False)  # Optional
    adding_end_time = serializers.DateTimeField(required=False)

    def validate(self, data):
        if data['has_limit'] and not data['limit']:
            raise serializers.ValidationError('Limit is required when has_limit is True')
        if data['is_private'] and not data['password'] and not data['invitational']:
            raise serializers.ValidationError('Password or invitational is required when is_private is True')
        if data['invitational'] and data['password']:
            raise serializers.ValidationError('only one of password or invitational is allowed')
        
        return data

    def create(self, validated_data):
        code = generate_unique_class_code()
        user = self.context['request'].user
        teacher = user.userprofile
        if 'password' in validated_data and validated_data['password']:
            validated_data['password'] = make_password(validated_data['password'])

        online_class = OnlineClass.objects.create(
            code=code,
            **validated_data
        )
        online_class.teachers.add(teacher)
        online_class.save()
        return online_class

        
    

