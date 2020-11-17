from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Watchlist, Comment
from .forms import CommentForm, BidForm, ListingForm

def index(request):

    listing = list(Listing.objects.all())

    product_names = []
    images = []
    descriptions = []
    price = []
    is_active = []

    for i in listing:
        product_names.append(i.product_name)
        descriptions.append(i.description)
        images.append(i.image_url)
        product_price = Bid.objects.get(listing = i.id)
        price.append(product_price.final_bid)
        is_active.append(i.is_active)

    products = list(zip(product_names, descriptions, images, price, is_active))

    return render(request, "auctions/index.html", {
        "products": products
    })

def product(request, name):
    listing = list(Listing.objects.all())

    product_names = []
    category = []

    for i in listing:
        product_names.append(i.product_name)
        category.append(i.category.all())

    if name in product_names:
        product = Listing.objects.get(product_name = name)
        name = product.product_name
        image = product.image_url
        description = product.description
        bid_user = product.user
        date = product.datetime
        categories = product.category.all()
        bid = Bid.objects.get(listing = product)
        last_bid_user = bid.user
        current_bids = bid.amount
        is_active = product.is_active
        current_user = User.objects.get(username = "icarus")
        user_watchlist = Watchlist.objects.get(user = current_user)
        comments_all = Comment.objects.filter(product = product)

        comment_user = []
        comment_content = []
        categories_list = []
        
        for comment in comments_all:
            comment_user.append(comment.user)
            comment_content.append(comment.body)

        comments = list(zip(comment_user, comment_content))

        for category in categories:
            categories_list.append(category.name)

        return render(request, 'auctions/product.html', {
            "name": name,
            "description": description, 
            "image": image,
            "bid_user": bid_user,
            "date": date,
            "categories": categories_list,
            "start_bid": bid.start_bid,
            "final_bid": bid.final_bid,
            "last_bid_user": last_bid_user,
            "current_bids": current_bids,
            "comment": CommentForm(),
            "comments": comments,
            "is_active": is_active,
            "new_bid": BidForm(initial = {'new_bid': bid.final_bid})
        })
    else:
        return render(request, 'auctions/content.html', {
			"error": f"This page '{name}' doesn't exist."
		})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
