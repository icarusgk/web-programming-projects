from django.contrib.auth.models import AbstractUser
from django.db import models

# User 
class User(AbstractUser):
    pass

# Auction Categories
class Category(models.Model):
    name = models.CharField(max_length=50)

# Listings
class Listing(models.Model):
    product_name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    image_url = models.URLField()  
    is_active = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

# Bids
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    start_bid = models.FloatField()
    final_bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)    

# Comments
class Comment(models.Model):
    body = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
