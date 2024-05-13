from django.db import models
from django.contrib.auth.models import User

class Messages(models.Model):
    sender = models.IntegerField()
    message = models.CharField(max_length=200)
    receiver = models.IntegerField()
    time_sent = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(null=True, blank=True)

class UserProfile(models.Model):
    profileid = models.IntegerField()
    picture = models.FileField( default='defaultpp.jpg')

    def __str__(self):
        return f'{self.id} Profile'
