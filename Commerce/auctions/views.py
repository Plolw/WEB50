from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import Listing, Bid, User, Comment

from .models import User

class ListingForm(forms.Form):
    ELECTRONICS = 'EL'
    HOME = 'HM'
    TOYS = 'TY'
    FASHION = 'FS'
    OTHER = 'OT'
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Title: max. 50 characters'}))
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'input',  'placeholder': 'Description: max. 500 characters'}))
    startingBid = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Starting Bid ($)'}))
    imgURL = forms.URLField(widget=forms.URLInput(attrs={'class': 'input', 'placeholder': 'Image URL'}))
    category = forms.ChoiceField(choices=[
        (ELECTRONICS, 'Electronics'), (HOME, 'Home'), (TOYS, 'Toys'), (FASHION, 'Fashion'), (OTHER, 'Other')
        ], 
        widget=forms.Select(attrs={'class': 'input',  'placeholder': 'Category'})
    )


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True),
        "title": "Active Listings"
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

@login_required()
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

@login_required
def new_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            currentBid = form.cleaned_data["startingBid"]
            imageURL = form.cleaned_data["imgURL"]
            category = form.cleaned_data["category"]
            listing = Listing(author=request.user, title=title, description=description,
                               currentBid=currentBid, imageURL=imageURL, category=category)
            listing.save()
            return HttpResponseRedirect(reverse(index))
        else:
            return render(request, "auctions/new_listing.html", {
                "form": form
            })
    else:
        form = ListingForm()
        return render(request, "auctions/new_listing.html", {
            "form": form
        })
    
def listing(request, listing):
    if request.method == "POST":
        ls = Listing.objects.get(pk=listing)
        ls.active = False
        ls.save()
        return HttpResponseRedirect(reverse(index))
    else:
        lis = Listing.objects.filter(id=listing).first()
        x = request.user.username
        bid = lis.bids.count()
        watchlisted = request.user.username in lis.watchers.values_list('username', flat=True)
        winner = lis.bids.all().order_by('-bid').first()
        return render(request, "auctions/listing.html", {
            "listing": lis,
            "watchlisted": watchlisted,
            "bid": bid,
            "author": lis.author,
            "winner": winner.bidder
        })

@login_required   
def place_bid(request, listing):
    if request.method == "POST":
        bid = request.POST["bid"]
        x = Listing.objects.filter(id=listing).first()
        x.currentBid = bid
        x.save()
        new_bid = Bid(bidder=request.user, bid=bid, listing=x)
        new_bid.save()
        return HttpResponseRedirect(reverse(index))
    
@login_required
def watchlist(request, listing):
    if request.method == "POST":
        lis = Listing.objects.get(pk=listing)
        if request.user.username in lis.watchers.values_list('username', flat=True):
            lis.watchers.remove(request.user)
        else:
            lis.watchers.add(request.user)
        return HttpResponseRedirect(reverse("listing", kwargs={"listing": listing}))
    
@login_required
def watchlistindex(request):
    if request.method == "GET":
        usr = request.user
        return render(request, "auctions/watchlist.html", {
            "listings": usr.watchlisted.all()
        })
    
def categories(request):
    x = Listing.CATEGORY_CHOICES
    print(Listing.CATEGORY_CHOICES)
    return render(request, "auctions/categories.html", {
        "categories": x
    })
    
def category(request, category):
    listings = Listing.objects.filter(category=category, active=True)
    return render(request, "auctions/index.html", {
        "title": category,
        "listings": listings
    })