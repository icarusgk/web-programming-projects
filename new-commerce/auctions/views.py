from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime as dt

from .models import User, Listing, Bid, Watchlist, Comment, Category
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
        price.append(i.last_price)
        is_active.append(i.is_active)

    products = list(zip(product_names, descriptions, images, price, is_active))
    
    
    return render(request, "auctions/index.html", {
        "products": products
    })

def active_listings(request):

    listing = list(Listing.objects.all())

    product_names = []
    images = []
    descriptions = []
    price = []

    for i in listing:
        if i.is_active is True:
            product_names.append(i.product_name)
            descriptions.append(i.description)
            images.append(i.image_url)
            product_price = Bid.objects.get(listing = i.id)
            price.append(product_price.final_bid)
        

    products = list(zip(product_names, descriptions, images, price))
    
    return render(request, "auctions/active.html", {
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
        # Assignation
        product = Listing.objects.get(product_name = name)
        name = product.product_name
        image = product.image_url
        description = product.description
        creator = product.creator
        date = product.datetime
        categories = product.category.all()
        all_bids = Bid.objects.filter(listing = product)
        last_bid_user = None

        if all_bids.last() is None:
            product.last_price = product.starting_price
            product.save()
        else:
            last_bid_user = all_bids.last().user
            product.last_price = all_bids.last().bid
            product.save()       

        current_bids = len(product.bid_set.all())
        is_active = product.is_active
        user_watchlist = Watchlist.objects.get(user = request.user)


        comments_all = Comment.objects.filter(product = product)
        comment_user = []
        comment_content = []


        categories_list = []

        watchlist_list = []

        for comment in comments_all:
            comment_user.append(comment.user)
            comment_content.append(comment.body)

        comments = list(zip(comment_user, comment_content))

        for category in categories:
            categories_list.append(category.name)

        for element in user_watchlist.product.all():
            watchlist_list.append(element.product_name)

        return render(request, 'auctions/product.html', {
            "name": name,
            "description": description,
            "image": image,
            "creator": creator,
            "date": date,
            "categories": categories_list,
            "start_bid": product.starting_price,
            "final_bid": product.last_price,
            "last_bid_user": last_bid_user,
            "current_bids": current_bids,
            "comment": CommentForm(),
            "comments": comments,
            "is_active": is_active,
            "watchlist": watchlist_list,
            "new_bid": BidForm(initial={'new_bid': product.last_price})
        })
    else:
        return render(request, 'auctions/product.html', {
            "error": f"This page '{name}' doesn't exist."
        })


@login_required
def new_item(request):
    return render(request, "auctions/new_item.html", {
        "form": ListingForm()
    })


@login_required
def input(request):

    if request.method == "POST":
        form = ListingForm(request.POST)
        listing = request.POST['title']
        user_name = request.POST['user_name']

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image_url = form.cleaned_data['image_url']
            initial_price = form.cleaned_data['bid']
            categories = form.cleaned_data['category']

            user = User.objects.get(username = user_name)

            new_listing = Listing(
                product_name = title,
                description = description,
                datetime = dt.datetime.now(),
                starting_price = initial_price,
                last_price = initial_price,
                image_url = image_url,
                is_active = True,
                creator = user)

            new_listing.save()

            for i in categories:
                category = Category.objects.get(id = i)
                new_listing.category.add(category)

            return product(request, listing)


def bid(request):
    if request.method == "POST":
        form = BidForm(request.POST)
        product = request.POST["page_name"]
        user_name = request.POST["user_name"]

        if form.is_valid():
            bid_amount = form.cleaned_data['new_bid']
            current_listing = Listing.objects.get(product_name = product)
            bid_user = User.objects.get(username = user_name)

            current_bid = Bid.objects.filter(listing = current_listing)

            if bid_amount > current_listing.last_price:
                new_bid = Bid(listing = current_listing, bid = bid_amount, user = bid_user)
                new_bid.save()

                
                current_listing.last_price = current_listing.bid_set.last().bid
                current_listing.save()

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return render(request, 'auctions/valid_amount.html', {
                    "message": "Enter a valid amount"
                })


def comment(request):
    if request.method == "POST":

        form = CommentForm(request.POST)
        product = request.POST['page_name']
        comment_username = request.POST['user_name']

        if form.is_valid():
            comment = form.cleaned_data['comment']
            current_user = User.objects.get(username=comment_username)
            current_product = Listing.objects.get(product_name=product)

            new_comment = Comment(
                user=current_user,
                body=comment,
                product=current_product)

            new_comment.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            return HttpResponseRedirect(reverse("index"))


def remove(request):
    if request.method == "POST":
        product = request.POST["remove_button"]
        item = Listing.objects.get(product_name=product)

        item.is_active = False
        item.save()

        return index(request)


def categories(request):
    categories = Category.objects.all()
    name = []
    category_list = []

    return render(request, 'auctions/categories.html', {
        "categories": categories
    })


def category(request, name):

    category_name = Category.objects.get(name=name)
    product_names = []
    closed_product_names = []
    for product in category_name.listing_set.all():
        if product.is_active == True:
            product_names.append(product.product_name)
        else:
            closed_product_names.append(product.product_name)

    return render(request, 'auctions/category.html', {
        "names": product_names,
        "inactive_names": closed_product_names,
        "title": name,
        "active": "Active Listings",
        "inactive": "Inactive Listings"
    })


def add_watchlist(request):
    if request.method == "POST":
        product_name = request.POST["product"]
        user = request.POST["user_name"]

        current_user = User.objects.get(username=user)
        current_product = Listing.objects.get(product_name=product_name)
        user_watchlist = Watchlist.objects.get_or_create(user=current_user)

        user_watchlist[0].product.add(current_product)
        user_watchlist[0].save()

        product_list = []

        for product in user_watchlist[0].product.all():
            product_list.append(product)

    return render(request, 'auctions/watchlist.html', {
        "title": "My Watchlist",
        "watchlist": product_list
    })


def remove_watchlist(request):
    if request.method == "POST":
        user = request.POST["user_name"]
        product = request.POST["product"]

        current_user = User.objects.get(username=user)
        current_product = Listing.objects.get(product_name=product)
        user_watchlist = Watchlist.objects.get(user=current_user)

        user_watchlist.product.remove(current_product)
        user_watchlist.save()

        return render(request, 'auctions/watchlist.html', {
            "product": product,
        })


def my_watchlist(request):
    if request.method == "POST":
        user_name = request.POST["user_name"]

        if user_name:
            user = User.objects.get(username = user_name)
            user_watchlist = Watchlist.objects.get(user = user)

            products_list = []
            for product in user_watchlist.product.all():
                products_list.append(product)

            return render(request, 'auctions/watchlist.html', {
                "watchlist": products_list,
                "active": "Active Listings"
            })
        else:
            return render(request, 'auctions/watchlist.html', {
                'message': "Please Login"
            })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)

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

            new_watchlist = Watchlist(user = user)
            new_watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
