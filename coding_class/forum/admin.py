from django.contrib.admin import register, ModelAdmin
from .models import *

@register(Forum)
class ForumAdmin(ModelAdmin):
    pass

@register(Message)
class MessageAdmin(ModelAdmin):
    pass

@register(Room)
class RoomAdmin(ModelAdmin):
    pass
