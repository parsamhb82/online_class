from django.db import models

class Activity(models.Model):
    online_class = models.ForeignKey('online_class.OnlineClass', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    max_score = models.IntegerField()

    def __str__(self) -> str:
        return self.name

class StudentActivity(models.Model):
    score = models.DecimalField(max_digits=5, decimal_places=2)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    question_answer = models.ForeignKey('question.QuestionAnswer', on_delete=models.CASCADE)