from rest_framework import serializers
from .models import Assignment, Question, Team, QuestionAnswer, Comment
from user.models import UserProfile
from activity.models import StudentActivity
from django.db.models import Sum

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
        
        return super().validate(data)
    
    def create(self, validated_data):
        if validated_data.get("is_team") == True and validated_data.get("teams_status") == 3:
            num_of_students_in_each_team = validated_data.get("num_students_in_each_team")
            assignment_id = validated_data.get("assignment")
            assignment = Assignment.objects.get(id=assignment_id)
            online_class = assignment.online_class
            student_activities = StudentActivity.objects.filter(activity__online_class=online_class)
            students_scores = student_activities.values('userprofile__user__username').annotate(total_score=Sum('score')).order_by('-total_score')
            
            # Format the scoresheet as a list of dictionaries
            scoresheet = [
                {'username': student['userprofile__user__username'], 'total_score': student['total_score']}
                for student in students_scores
            ]
            num_of_students = len(scoresheet)
            num_of_teams = num_of_students // num_of_students_in_each_team ##need to get finished
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
    
class CreateTeamSerializer(serializers.ModelSerializer):
    # Field to accept usernames
    usernames = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )

    class Meta:
        model = Team
        fields = ['name', 'question', 'usernames']  # Add other fields if necessary

    def create(self, validated_data):
        # Extract usernames from the validated data
        usernames = validated_data.pop('usernames')

        # Create the Team instance
        team = Team.objects.create(**validated_data)

        # Retrieve UserProfile instances and add them to the team
        user_profiles = UserProfile.objects.filter(user__username__in=usernames)
        team.users.set(user_profiles)

        return team

    def validate_usernames(self, value):
        # Ensure all usernames exist in the system
        invalid_usernames = [username for username in value if not UserProfile.objects.filter(user__username=username).exists()]
        if invalid_usernames:
            raise serializers.ValidationError(f"These usernames are invalid: {', '.join(invalid_usernames)}")
        return value


class CreateCommentSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["question_answer", "text"]
        
    def validate(self, data):
        if data.get("text") == '':
            raise serializers.ValidationError("text is required")
        return data
    
    def create(self, validated_data):
        question_asnwer_id = validated_data.get("question_answer")
        question_answer = QuestionAnswer.objects.get(id=question_asnwer_id)
        user = self.context.get("request").user
        user_profile = UserProfile.objects.get(user=user)
        online_class = question_answer.question.assignment.online_class
        if user_profile not in online_class.teachers.all() or user_profile not in online_class.mentors.all():
            raise serializers.ValidationError("You are not allowed to comment")
        comment = Comment.objects.create(question_answer=question_answer, text=validated_data.get("text"), user_profile=user_profile)
        return comment
    
class StudentAnswerScoreSerilizer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ["question_answer", "score"]

    def validate(self, data):
        if data.get("score") == '' or data.get("score") < 0 or type(data.get("score")) != int:
            raise serializers.ValidationError("given score is not valid")
        return data
