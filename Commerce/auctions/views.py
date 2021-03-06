from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime as dt

from .models import User, Listing, Category, Bid, Comment, Watchlist
from .forms import ListingForm, CommentForm, BidForm

global_username = []

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

def content(request, name):
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
		watchlist_products = []
		categories_list = []

		for comment in comments_all:
			comment_user.append(comment.user)
			comment_content.append(comment.body)

		comments = list(zip(comment_user, comment_content))			

		for product in user_watchlist.product.all():
			watchlist_products.append(product.product_name)

		for category in categories:
			categories_list.append(category.name)
		
		return render(request, 'auctions/content.html', {
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
			"watchlist": watchlist_products,
			"comment": CommentForm(),
			"comments": comments,
			"is_active": is_active,
			"new_bid": BidForm(initial={'new_bid': bid.final_bid})
		})
	else:
		return render(request, 'auctions/content.html', {
			"error": f"This page '{name}' doesn't exist."
		})

@login_required
def forms(request):
	return render(request, "auctions/forms.html", {
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
			bid = form.cleaned_data['bid']
			categories = form.cleaned_data['category']			
			
			user = User.objects.get(username = user_name)

			new = Listing(
				product_name = title, 
				description = description,
				datetime = dt.datetime.now(),
				image_url = image_url, 
				is_active = True,
				user = user)

			new.save()

			for i in categories:
				category = Category.objects.get(id = i)
				new.category.add(category)

			new_bid = Bid(user = user, listing = new, start_bid = bid, final_bid = bid)
			new_bid.save()

			return content(request, listing)

def bid(request):
	if request.method == "POST":
		form = BidForm(request.POST)
		product = request.POST["page_name"]
		user_name = request.POST["user_name"]

		if form.is_valid():
			bid = form.cleaned_data['new_bid']
			current_listing = Listing.objects.get(product_name=product)
			user = User.objects.get(username=user_name)

			new_bid = Bid.objects.get(listing=current_listing)

			if bid > new_bid.final_bid:
				new_bid.amount += 1
				new_bid.final_bid = bid
				new_bid.user = user
				new_bid.save()
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
		item = Listing.objects.get(product_name = product)

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
	
	category_name = Category.objects.get(name = name)
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

		current_user = User.objects.get(username = user)
		current_product = Listing.objects.get(product_name = product_name)
		user_watchlist = Watchlist.objects.get_or_create(user = current_user)

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

		current_user = User.objects.get(username = user)
		current_product = Listing.objects.get(product_name = product)
		user_watchlist = Watchlist.objects.get(user = current_user)

		user_watchlist.product.remove(current_product)
		user_watchlist.save()

		return render(request, 'auctions/watchlist.html', {
			"product": product,			
		})


def my_watchlist(request):

	user = User.objects.get(username = "nicolle")
	print(global_username)
	user_watchlist = Watchlist.objects.get(user = user)

	products_list = []
	for product in user_watchlist.product.all():
		products_list.append(product)

		
	return render(request, 'auctions/watchlist.html', {
		"watchlist": products_list,
		"active": "Active Listings"
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
		except IntegrityError:
			return render(request, "auctions/register.html", {
				"message": "Username already taken."
			})
		login(request, user)
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "auctions/register.html")
