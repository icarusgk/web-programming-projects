from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Auction Categories

class Category(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)

# Bids
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    start_bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)    

# Comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)



# Listings
class Listing(models.Model):
    product_name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    start_bid = models.FloatField(max_length=16)
    image_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
