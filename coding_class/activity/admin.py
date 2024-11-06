from django.contrib.admin import register, ModelAdmin

from .models import *

@register(Activity)
class ActivityAdmin(ModelAdmin):
    pass

@register(StudentActivity)
class StudentActivityAdmin(ModelAdmin):
    pass

