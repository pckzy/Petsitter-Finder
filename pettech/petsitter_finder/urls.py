from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("login/", views.LoginView.as_view(), name="login_view"),
]