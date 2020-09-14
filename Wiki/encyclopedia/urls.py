from . import views
from django.urls import path

app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.content, name="content"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("create_entry", views.create_entry, name="create_entry"),
    path("edit/", views.edit, name="edit"),
    path("edit_page/", views.edit_page, name="edit_page"),
    path("random/", views.random, name="random")
]
