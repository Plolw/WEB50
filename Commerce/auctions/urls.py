from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new_listing"),
    path("listing/<int:listing>", views.listing, name="listing"),
    path("place_bid/<int:listing>", views.place_bid, name="place_bid"),
    path("watchlist", views.watchlistindex, name="watchlistindex"),
    path("watchlist/<int:listing>", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("comment/<int:listing>", views.comment, name="comment")
]
