from django.urls import path
from .views import CreateOnlineClass, UpdateOnlineClass, AddMentorToClass, OnlineClassViewStudetsView

urlpatterns = [
    path('create/', CreateOnlineClass.as_view()),
    path('update/<int:pk>/', UpdateOnlineClass.as_view()),
    path('add-mentor/', AddMentorToClass.as_view()),
    path('view-students/<int:pk>/', OnlineClassViewStudetsView.as_view()),
]