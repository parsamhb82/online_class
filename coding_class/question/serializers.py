from rest_framework import serializers
from .models import Assignment, Question, Team, QuestionAnswer

class AssignmentSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = "__all__"

class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
    
    def validate(self, data):
        if data.get('has_time_limit') and not data.get('first_deadline'):
            raise serializers.ValidationError("first deadline is required")
        if data.get('has_upload_limit') and not data.get('upload_limit') == '':
            raise serializers.ValidationError("upload limit is required")
        if data.get('has_upload_limit') and data.get('has_time_limit'):
            if data.get('first_deadline') > data.get('second_deadline'):
                raise serializers.ValidationError("first deadline must be before second deadline")
        if data.get('second_deadline') and not data.get('penalty_hour') :
            raise serializers.ValidationError("penalty hour is required")
        if data.get("second_deadline") and not data.get('penalty'):
            raise serializers.ValidationError("penalty is required")
        if data.get('is_team') == True and not data.get('teams_status'):
            raise serializers.ValidationError("teams status is required")
        
        return data
    
    def create(self, validated_data):
        question = Question.objects.create(**validated_data)
        return question
    

class CreateTextQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ["question", "text"]
    
    def validate(self, data):
        if data.get("text") == '':
            raise serializers.ValidationError("text is required")
        if data.get("file"):
            raise serializers.ValidationError("file is not allowed")
        return data


class CreateFileQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ["question", "file"]
    
    def validate(self, data):
        if data.get("text") :
            raise serializers.ValidationError("text is  not allowed")
        if not data.get("file"):
            raise serializers.ValidationError("file is required")
        return data
    
