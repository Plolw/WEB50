from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name="following")

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=1000)
    dateTime = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()

    def __str__(self):
        return f"{self.author}, {self.content}, {self.dateTime}, {self.likes}"
    
    def serialize(self):
        return {
            "author": self.author,
            "content": self.content,
            "dateTime": self.dateTime,
            "likes": self.likes
        }