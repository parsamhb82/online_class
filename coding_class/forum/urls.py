from django.urls import path
from .views import CreateRoomView, CreateMessageView, UpdateMessageView, DeleteMessageView, DeleteRoomView

urlpatterns = [
    path('create-room/', CreateRoomView.as_view()),
    path('create-message/', CreateMessageView.as_view()),
    path('update-message/<int:pk>/', UpdateMessageView.as_view()),
    path('delete-message/<int:pk>/', DeleteMessageView.as_view()),
    path('delete-room/<int:pk>/', DeleteRoomView.as_view()),
]