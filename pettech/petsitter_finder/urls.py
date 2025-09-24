from django.urls import path

from . import views

urlpatterns = [
    path("", views.test, name="test"),
    path("login/", views.LoginView.as_view(), name="login_view"),
]