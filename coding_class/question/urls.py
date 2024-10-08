from django.urls import path
from .views import ShowAssignments, CreateAssignment, CreateQuestion, CreateFileQuestionAnswer, CreateTextQuestionAnswer, CreateTeamView

urlpatterns = [
    path('assignments/create/', CreateAssignment.as_view()),
    path('assignments/show/', ShowAssignments.as_view()),
    path('create/', CreateQuestion.as_view()),
    path('create-file-answer/', CreateFileQuestionAnswer.as_view()),
    path('create-text-answer/', CreateTextQuestionAnswer.as_view()),
    path('create-team/', CreateTeamView.as_view()),
]