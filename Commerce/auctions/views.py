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
        "listings": Listing.objects.all()
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

def new_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            startingBid = form.cleaned_data["startingBid"]
            imageURL = form.cleaned_data["imgURL"]
            category = form.cleaned_data["category"]
            listing = Listing(author=request.user, title=title, description=description,
                               startingBid=startingBid, imageURL=imageURL, category=category)
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