from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# Listings
class Listing(models.Model):
    product_name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    start_bid = models.FloatField(max_length=16)
    image_url = models.URLField()

# Bids
class Bid(models.Model):
    pass

# Comments
class Comment(models.Model):
    pass

# Auction Categories
class Category(models.Model):
    pass

class Auction(models.Model):
    pass