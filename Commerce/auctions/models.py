from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    ELECTRONICS = 'EL'
    HOME = 'HM'
    TOYS = 'TY'
    FASHION = 'FS'
    OTHER = 'OT'
    CATEGORY_CHOICES = [(ELECTRONICS, 'Electronics'), (HOME, 'Home'), (TOYS, 'Toys'), (FASHION, 'Fashion'), (OTHER, 'Other')]
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    startingBid = models.IntegerField()
    imageURL = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=OTHER)