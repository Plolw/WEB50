from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
@login_required()   
def create(request):
    print("hello")
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    data = json.loads(request.body)
    content = data.get("content")
    post = Post(author=request.user, content=content, likes=0)
    post.save()
    return JsonResponse({"message": "Post posted succesfully!"}, status=201)


def posts(request, category):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    if category == "allposts":
        posts = Post.objects.all()
    elif category == "following":
        user = request.user 
        following = user.following
        posts = Post.objects.filter(author__in=following).all()
    else:
        return JsonResponse({"error": "Requested page does not exist"}, status=400)
    posts = posts.order_by("-dateTime").all()
    return JsonResponse([pst.serialize() for pst in posts], safe=False)


def post(request, id):
    try:
        author = User.objects.get(id=id)
        posts = Post.objects.filter(author=author)
    except posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == "GET":
        return JsonResponse([pst.serialize() for pst in posts], safe=False)
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            p = Post.objects.get(id=id)
            p.content = data["content"]
        if data.get("likes") is not None:
            p = Post.objects.get(id=id)
            p.content = data["likes"]
        p.save()
        return HttpResponse(status=201)
    else:
        return JsonResponse({"error": "Must use GET or PUT methods"}, status=404)
    
def profile(request, id):
    if request.method != "GET":
        return JsonResponse({"error": "Must use GET method"}, status=404)
    try:
        profile = User.objects.get(id=id)
    except profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found."}, status=404)
    return JsonResponse(profile.serialize(), safe=False)

def follow(request, user_id):
    print("1")
    if request.method != "PUT":
        return JsonResponse({"error": "Must use PUT mehtod"}, status=404)
    usr = User.objects.get(id=user_id)
    usr.followers.add(request.user)
    return JsonResponse({"message": f"{usr.username} followed succesfully"})