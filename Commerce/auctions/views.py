from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime as dt

from .models import User, Listing, Category, Bid, Comment
from .forms import ListingForm, CommentForm, BidForm

bid_list = []

def index(request):

	listings = list(Listing.objects.values())

	return render(request, "auctions/index.html", {
		"listt": listings,
		"comment": CommentForm()
	})

def product(request, name):

	listing = list(Listing.objects.all())


	product_names = []
	descriptions = []
	users = []


	for i in listing:
		product_names.append(i.product_name)
		descriptions.append(i.description)
		users.append(i.user.username)

	products = list(zip(product_names, descriptions, users))

	if name in product_names:
		product = Listing.objects.get(product_name=name)
		name = product.product_name
		image = product.image_url
		description = product.description
		user = product.user
		date = product.datetime
		categories = product.category.values()
		bid = Bid.objects.get(listing=product)
		current_bids = len(bid_list)
		comments = Comment.objects.filter(product=product)
		
		return render(request, 'auctions/content.html', {
			"name": name,
			"description": description,
			"image": image,
			"user": user,
			"date": date,
			"categories": categories,
			"start_bid": bid.start_bid,
			"final_bid": bid.final_bid,
			"current_bids": current_bids,
			"comment": CommentForm(),
			"comments": comments,
			"new_bid": BidForm()
		})
	else:
		return render(request, 'auctions/content.html', {
			"error": f"This page '{name}' doesn't exist."
		})

def forms(request):
	return render(request, "auctions/forms.html", {
		"form": ListingForm()
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
									 
			user = User.objects.get(username="icarus")

			new = Listing(
				product_name = title, 
				description = description,
				datetime = dt.datetime.now(),
				image_url = image_url, 
				is_active = True,
				user = user)

			new.save()

			for i in categories:
				category = Category.objects.get(id=i)
				new.category.add(category)

			new_bid = Bid(user = user, listing = new, start_bid = bid, final_bid = bid)
			new_bid.save()

			return render(request, "auctions/index.html", {
				"message": "Congratulations!",
				"cat": categories
			})

def bid(request):
	if request.method == "POST":
		form = BidForm(request.POST)
		product = request.POST['page_name']

		if form.is_valid():
			bid = form.cleaned_data['new_bid']
			current_listing = Listing.objects.get(product_name=product)
			user = User.objects.get(username="paola")

			new_bid = Bid.objects.get(listing=current_listing)

			if bid > new_bid.final_bid:
				bid_list.append(bid)
				new_bid.final_bid = bid
				new_bid.save()
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
			else:
				return HttpResponse("Enter a valid amount")
			

def comment(request):
	if request.method == "POST":

		form = CommentForm(request.POST)
		product = request.POST['page_name']

		if form.is_valid():
			comment = form.cleaned_data['comment']
			current_user = User.objects.get(username="paola")
			current_product = Listing.objects.get(product_name=product)

			new_comment = Comment(
				user=current_user, 
				body=comment, 
				product=current_product)
				
			new_comment.save()		

			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

		else:
			return HttpResponseRedirect(reverse("index"))


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
