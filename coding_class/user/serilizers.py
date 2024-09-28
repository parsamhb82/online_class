from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class UserRegisterSerilizer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)
    image = serializers.ImageField(required=False)
    description = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirmation', 'email', 'image', 'description']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Passwords do not match')
        return data
    
    def create(self, validated_data):
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError('Username already exists')
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError('Email already exists')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user_profile = UserProfile.objects.create(
            user=user,
            description=validated_data.get('description', ''),
            picture=validated_data.get('image', None)
        )
        return user
    
class UserChangePasswordSerilizer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirmation = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'new_password_confirmation']
    
    def validate(self, data):
        user = self.instance
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError('Old password is incorrect')
        
        if data['new_password'] != data['new_password_confirmation']:
            raise serializers.ValidationError('New passwords do not match')
        
        return data
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['description', 'picture']
        
