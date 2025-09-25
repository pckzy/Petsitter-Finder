from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("back/", views.back, name="back"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("sitter_detail/<int:id>", views.SitterView.as_view(), name="sitter"),
    path("booking_form/<int:sitter_id>", views.BookingFormView.as_view(), name="booking_form"),
    path("booking_detail/<int:booking_id>", views.BookingDetailView.as_view(), name="booking_detail"),
    path('review/create/<int:booking_id>/', views.ReviewCreateView.as_view(), name='review_create'),
    path('bookings/', views.user_bookings, name='user_bookings'),
    path('bookings/cancel/<int:booking_id>/', views.cancel_booking, name='cancel'),
    path('bookings/accept/<int:booking_id>/', views.accept_booking, name='accept'),
    path('bookings/finish/<int:booking_id>/', views.finish_booking, name='finish'),
]