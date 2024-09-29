from django.db import models
from user.models import UserProfile
from django.utils.timezone import now
class OnlineClass(models.Model):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(UserProfile, blank=True, related_name="teachers")
    mentors = models.ManyToManyField(UserProfile, blank=True, related_name="mentors")
    students = models.ManyToManyField(UserProfile, blank=True, related_name="students")
    is_private = models.BooleanField(default=True)
    has_limit = models.BooleanField(default=False)
    limit = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    invitational = models.BooleanField(blank=True)
    password = models.CharField(max_length=100)
    adding_start_time = models.DateTimeField(blank=True, default=now())
    adding_end_time = models.DateTimeField(blank=True)
    available = models.BooleanField(default=True)


