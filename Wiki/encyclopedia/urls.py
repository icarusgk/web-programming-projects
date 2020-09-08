from . import views
from django.urls import path

# app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.content, name="content"),
    path("create/", views.create, name="create"),
    path("random/", views.random, name="random"),
]
