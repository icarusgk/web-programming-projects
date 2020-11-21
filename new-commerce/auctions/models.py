from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Users
class User(AbstractUser):
    pass


# Category

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


# Listing

class Listing(models.Model):
    product_name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    datetime = models.DateTimeField(default = timezone.now)
    starting_price = models.FloatField(default=0)
    last_price = models.FloatField(default=0)
    image_url = models.URLField()
    is_active = models.BooleanField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.product_name} - uploaded by: '{self.creator}' on {self.datetime}"


# Bids
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listing.product_name} - ({self.user}) bidded: {self.bid}"


# Comments

class Comment(models.Model):
    body = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} commented on product ({self.product})"


# Watchlist

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Listing)

    def __str__(self):
        return f"{self.user}'s Watchlist"
