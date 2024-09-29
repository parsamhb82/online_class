from django.urls import path
from .views import CreateOnlineClass

urlpatters = [
    path('create/', CreateOnlineClass.as_view()),
]