from django.urls import path
from .views import CreateOnlineClass, UpdateOnlineClass, AddMentorToClass, OnlineClassViewStudetsView, AddTeacherToClass
from .views import RemoveStudentFromClass, EnterTheClassByPasswordView, SendInviteView, ConfirmEnrollmentView, StudentClassView
from .views import StudentAddView, StudentsScoreSheet
urlpatterns = [
    path('create/', CreateOnlineClass.as_view()),
    path('update/<int:pk>/', UpdateOnlineClass.as_view()),
    path('add-mentor/', AddMentorToClass.as_view()),
    path('view-students/<int:pk>/', OnlineClassViewStudetsView.as_view()),
    path('add-teacher/', AddTeacherToClass.as_view()),
    path('remove-student/', RemoveStudentFromClass.as_view()),
    path('enter-class-by-password/', EnterTheClassByPasswordView.as_view()),
    path('send-invite/', SendInviteView.as_view()),
    path('confirm-enrollment/', ConfirmEnrollmentView.as_view()),
    path('student-class-view/', StudentClassView.as_view()),
    path('add-student/', StudentAddView.as_view()),
    path('students-score-sheet/', StudentsScoreSheet.as_view()),

]