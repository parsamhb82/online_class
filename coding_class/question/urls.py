from django.urls import path
from .views import ShowAssignments, CreateAssignment

urlpatterns = [
    path('assignments/create/', CreateAssignment.as_view()),
    path('assignments/show/', ShowAssignments.as_view()),
]