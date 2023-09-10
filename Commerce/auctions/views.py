from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User

class ListingForm (forms.Form):
    ELECTRONICS = 'EL'
    HOME = 'HM'
    TOYS = 'TY'
    FASHION = 'FS'
    OTHER = 'OT'
    title = forms.CharField(label="title", max_length=20)
    description = forms.CharField(label="description", max_length=200, widget=forms.Textarea)
    startingBid = forms.NumberInput()
    imgURL = forms.URLField()
    category = forms.ChoiceField(choices=[
        (ELECTRONICS, 'Electronics'), (HOME, 'Home'), (TOYS, 'Toys'), (FASHION, 'Fashion'), (OTHER, 'Other')
        ], 
        widget=forms.Select()
    )


def index(request):
    return render(request, "auctions/index.html")


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

def new_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if (form.is_valid):
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            startingBid = form.cleaned_data["startingBid"]
            imageURL = form.cleaned_data["imageURL"]
            category = form.cleaned_data["category"]
        else:
            return render(request, "auctions/new_listing.html", {
                "form": form
            })
    else:
        form = ListingForm()
        return render(request, "auctions/new_listing.html", {
            "form": form
        })