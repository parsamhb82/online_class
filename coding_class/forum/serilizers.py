from rest_framework import serializers
from .models import Forum, Room, Message


class CreateRoomSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'forum']

class CreateMessageSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'room']

class UpdateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']