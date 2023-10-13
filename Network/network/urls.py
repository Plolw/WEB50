from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.create, name="create"),
    path("postscat/<str:category>/<int:page>", views.posts, name="posts"),
    path("posts/<int:id>/<int:page>", views.post, name="post"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("edit/<int:id>", views.edit, name="edit")
]
