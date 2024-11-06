from django.contrib.admin import register, ModelAdmin
from .models import OnlineClass, Enrollment
@register(OnlineClass)
class OnlineClassAdmin(ModelAdmin):
    pass

@register(Enrollment)
class EnrollmentAdmin(ModelAdmin):
    pass

