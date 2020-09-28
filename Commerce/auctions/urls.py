from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("forms", views.forms, name="forms"),
    path("input", views.input, name="input"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
