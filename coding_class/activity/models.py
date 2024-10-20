from django.db import models

class Activity(models.Model):
    online_class = models.ForeignKey('online_class.OnlineClass', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    max_score = models.IntegerField()

    def __str__(self) -> str:
        return self.name

