from django.db import models

class Forum(models.Model):
    online_class = models.ForeignKey('online_class.OnlineClass', on_delete= models.CASCADE)
    
class Room(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    creator = models.ForeignKey("user.UserProfile", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey("user.UserProfile", on_delete=models.PROTECT)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

