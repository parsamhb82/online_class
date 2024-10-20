from .views import CreateActivityView, DestroyActivityView
from django.urls import path

urlpatterns = [
    path('create/', CreateActivityView.as_view(), name='create-activity'),
    path('delete/<int:pk>/', DestroyActivityView.as_view(), name='delete-activity'),
]