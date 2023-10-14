from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name="following")
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followers": [follower.id for follower in self.followers.all()],
            "following": [following.id for following in self.following.all()],
            "liked": [post.id for post in self.liked.all()]
        }

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=1000)
    dateTime = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked")

    def __str__(self):
        return f"{self.author}, {self.content}, {self.dateTime}, {self.likes}"
    
    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "author_id": self.author.id,
            "content": self.content,
            "dateTime": self.dateTime.strftime("%b %d %Y, %I:%M %p"),
            "likes": [liker.id for liker in self.likes.all()]
        }