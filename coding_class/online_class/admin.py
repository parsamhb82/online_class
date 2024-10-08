from django.contrib.admin import register, ModelAdmin
from .models import OnlineClass
@register(OnlineClass)
class OnlineClassAdmin(ModelAdmin):
    pass
