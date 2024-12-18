from django.urls import path
from .views import UserRegisterView, Login, Refresh, ChangePasswordView, UserProfileUpdateView

urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('login/', Login.as_view()),
    path('refresh/', Refresh.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('update-profile/', UserProfileUpdateView.as_view()),

]