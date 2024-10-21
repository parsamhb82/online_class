from django.db import models

class Assignment(models.Model):
    name = models.CharField(max_length=100)
    online_class = models.ForeignKey("online_class.OnlineClass", on_delete=models.CASCADE)
    activity = models.ForeignKey("activity.Activity", on_delete=models.CASCADE, blank=True, null=True)


class Question(models.Model):
    ANSWER_FORMAT_CHOICES = [
        ('text', 'Text'),
        ('file', 'File'),
        ('code', 'Code'),
    ]
    answer_format = models.CharField(choices=ANSWER_FORMAT_CHOICES, max_length=10)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    has_time_limit = models.BooleanField(default=False)
    has_upload_limit = models.BooleanField(default=False)
    first_deadline = models.DateTimeField(blank=True)
    second_deadline = models.DateTimeField(blank=True)
    penalty_hour = models.IntegerField(blank=True)
    penalty = models.IntegerField(blank=True)
    upload_limit = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    in_bank = models.BooleanField(default=False)
    max_score = models.IntegerField(default=100)
    is_team = models.BooleanField(default=False)
    teams_status = models.IntegerField(blank=True, null=True)
    scoring_way = models.IntegerField(default=0)
    num_students_in_each_team = models.IntegerField(blank=True, null=True, default=1)

class Team(models.Model):
    name = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    users = models.ManyToManyField("user.UserProfile")

class QuestionAnswer(models.Model):
    student = models.ForeignKey("user.UserProfile", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    file = models.FileField(upload_to='question_answers/', blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)

class Comment(models.Model):
    question_answer = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE)
    user = models.ForeignKey("user.UserProfile", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



