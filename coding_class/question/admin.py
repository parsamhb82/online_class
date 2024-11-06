from django.contrib.admin import ModelAdmin, register
from .models import Assignment, Question, Team, QuestionAnswer, Comment

@register(Question)
class QuestionAdmin(ModelAdmin):
    pass

@register(Assignment)
class AssignmentAdmin(ModelAdmin):
    pass

@register(Team)
class TeamAdmin(ModelAdmin):
    pass

@register(QuestionAnswer)
class QuestionAnswerAdmin(ModelAdmin):
    pass

@register(Comment)
class CommentAdmin(ModelAdmin):
    pass