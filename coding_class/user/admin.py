from django.contrib.admin import register, ModelAdmin
from .models import UserProfile

@register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    pass
