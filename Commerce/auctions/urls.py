from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<str:name>", views.content, name="content"),
    path("categories", views.categories, name="categories"),
    path("category/<str:name>", views.category, name="category"),
    path("add-watchlist", views.add_watchlist, name="add-watchlist"),
    path("remove-watchlist", views.remove_watchlist, name="remove-watchlist"),
    path("my-watchlist/<str:username>", views.my_watchlist, name="my-watchlist"),
    path("forms", views.forms, name="forms"),
    path("input", views.input, name="input"),
    path("bid", views.bid, name="bid"),
    path("remove", views.remove, name="remove"),
    path("comment", views.comment, name="comment"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
