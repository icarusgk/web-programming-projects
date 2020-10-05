from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime as dt

# User 
class User(AbstractUser):
    pass

# Auction Categories
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

# Listings
class Listing(models.Model):
    product_name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    datetime = models.DateField(default=dt.datetime.now)
    image_url = models.URLField()  
    is_active = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    
    def __str__(self):
        return f"{self.product_name} - ({self.user}) on {self.datetime}"

# Bids
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    start_bid = models.FloatField()
    final_bid = models.FloatField()
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listing.product_name} - ({self.user}) Initial: {self.start_bid} / Final: {self.final_bid}"

# Comments
class Comment(models.Model):
    body = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
