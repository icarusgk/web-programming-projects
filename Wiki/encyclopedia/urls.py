from . import views
from django.urls import path

app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.content, name="content"),
    path("search/", views.search, name="search")
]
