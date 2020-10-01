from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Bid
from .forms import ListingForm, CommentForm

listing = list(Listing.objects.all())
listings = list(Listing.objects.values())
keys = ["product_name", "description", "user_id"]

product_names = []
descriptions = []
users = []


for i in listing:
    product_names.append(i.product_name)
    descriptions.append(i.description)
    users.append(i.user.username)

products = list(zip(product_names, descriptions, users))

def index(request):
   
    
    return render(request, "auctions/index.html", {
        "list": products,
        "listt": listings,
        "comment": CommentForm()
    })

def content(request, name):
    if name in names:
        return render(request, 'auctions/content.html', {
            "name": name
        })

def forms(request):
    return render(request, "auctions/forms.html", {
        "form": ListingForm
    })

def input(request):
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image_url = form.cleaned_data['image_url']
            bid = form.cleaned_data['bid']
            categories = form.cleaned_data['category']

            # for i in categories:
            #     list_categories = Category.objects.get(id=i)
                         
            category = Category.objects.get(name="Health")

            user = User.objects.get(username="icarus")

            new = Listing(
                product_name = title, 
                description = description,
                image_url = image_url, 
                is_active = True,
                user = user, 
                category = category)
            new.save()

            new_bid = Bid(user = user, listing = new, start_bid = bid, final_bid = bid)
            new_bid.save()

            return render(request, "auctions/input.html", {
                "message": "Congratulations!"
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
