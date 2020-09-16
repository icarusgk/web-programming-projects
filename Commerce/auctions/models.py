from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Auction Listings
class Listing(models.Model):
    pass
# Bids
class Bid(models.Model):
    pass

# Comments
class Comment(models.Model):
    pass

# Auction Categories
class Category(models.Model):
    pass