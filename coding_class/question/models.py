from django.db import models

class Assignment(models.Model):
    name = models.CharField(max_length=100)
    online_class = models.ForeignKey("class.OnlineClass")


class Question(models.Model):
    answer_format = models.CharField(max_length=4)
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
    teams_status = models.IntegerField(default=0)
    scoring_way = models.IntegerField(default=0)

class Team(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    users = models.ManyToManyField("user.UserProfile")


