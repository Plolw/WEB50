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
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    currentBid = models.IntegerField()
    imageURL = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=OTHER)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlisted")

    def __str__(self):
        return f"{self.title}: {self.description}: {self.currentBid}: {self.category}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=0, related_name="bids")

    def __str__(self):
        return f"{self.bid}"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.comment}"
    