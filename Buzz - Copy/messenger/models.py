from django.db import models
from django.contrib.auth.models import User

class Messages(models.Model):
    sender = models.IntegerField()
    message = models.CharField(max_length=200)
    receiver = models.IntegerField()
    time_sent = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(null=True, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.FileField(upload_to='user_pictures', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'
