from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("NewPage", views.new_page, name="new_page"),
    path("wiki/edit/<str:x>", views.edit, name="edit")
]
