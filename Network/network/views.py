from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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


def posts(request, category, page):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    if category == "allposts":
        posts = Post.objects.all()
    elif category == "following":
        user = request.user 
        following = user.following.all()
        posts = Post.objects.filter(author__in=following).all()
    else:
        return JsonResponse({"error": "Requested page does not exist"}, status=400)
    posts = posts.order_by("-dateTime").all()
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)
    print(page)
    print(paginator.num_pages)
    if  page < 1:
        return JsonResponse({"error": "page < 1"}, status=404)
    if  page > paginator.num_pages:
        return JsonResponse({"error": "page > max"}, status=404)
    print("A")
    return JsonResponse([pst.serialize() for pst in page_obj], safe=False)


def post(request, id, page):
    if request.method == "GET":
        try:
            author = User.objects.get(id=id)
            posts = Post.objects.filter(author=author)
        except posts.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        posts = posts.order_by("-dateTime").all()
        paginator = Paginator(posts, 10)
        page_obj = paginator.get_page(page)
        if  page < 1:
            return JsonResponse({"error": "page < 1"}, status=404)
        if  page > paginator.num_pages:
            return JsonResponse({"error": "page > max"}, status=404)
        return JsonResponse([pst.serialize() for pst in page_obj], safe=False)
    
def profile(request, id):
    if request.method != "GET":
        return JsonResponse({"error": "Must use GET method"}, status=404)
    try:
        profile = User.objects.get(id=id)
    except profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found."}, status=404)
    return JsonResponse(profile.serialize(), safe=False)

@login_required()
def follow(request, id):
    print(request.user)
    print("0")
    if request.method != "PUT":
        return JsonResponse({"error": "Must use PUT mehtod"}, status=404)
    if request.user.id != id:
        usr = User.objects.get(id=id)
        if request.user not in usr.followers.all():
            usr.followers.add(request.user)
            return JsonResponse({"message": f"{usr.username} followed succesfully!"}, status=201)
        else:
            usr.followers.remove(request.user)
            return JsonResponse({"message": f"{usr.username} unfollowed succesfully!"}, status=201)
    else:
        return JsonResponse({"error": "Can't follow yourself"})
    
@login_required
def edit(request, id):
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            p = Post.objects.get(id=id)
            p.content = data["content"]
        if data.get("liker") is not None:
            p = Post.objects.get(id=id)
            if request.user in p.likes.all():
                p.likes.remove(request.user)
            else:
                p.likes.add(request.user)
        p.save()
        return JsonResponse({"message": "PUT request submitted succesfully!"}, status=201)
    else:
        return JsonResponse({"error": "Must use GET or PUT methods"}, status=404)