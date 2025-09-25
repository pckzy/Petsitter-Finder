from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q

from .forms import *

from decimal import Decimal

# Create your views here.
class LoginView(View):
    def get(self, request):
        user_form = LoginForm()

        return render(request, 'login.html', {
            'form': user_form
        })

    def post(self, request):
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            user = user_form.cleaned_data['user']
            request.session['user_id'] = user.id
            return redirect('/home')
        
        return render(request, 'login.html', {
            'form': user_form
        })
    

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect(request.META.get('HTTP_REFERER', '/'))

def back(request):
    previous_url = request.session.get('previous_url', '/')
    return redirect(previous_url)

def home(request):
    pet_types = PetType.objects.all()
    sitters = PetSitter.objects.all()
    
    search_query = request.GET.get('search', '')
    pet_type = request.GET.get('pet_type', '')
    location = request.GET.get('location', '')

    request.session['previous_url'] = request.META.get('HTTP_REFERER')

    if search_query or pet_type or location:
        if search_query:
            sitters = sitters.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query)
            )
        if pet_type:
            sitters = sitters.filter(pet_types__id=pet_type)
        if location:
            sitters = sitters.filter(location__icontains=location)

    context = {
        'pet_types': pet_types,
        'sitters': sitters,
        'search_query': search_query,
        'selected_pet_type': pet_type,
        'selected_location': location,
    }

    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(pk=user_id)
        context['user'] = user
        bookings = Booking.objects.filter(customer=user).order_by('-created_at')[:1]
        context['bookings'] = bookings

    return render(request, 'home.html', context)


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm(request.POST)
        return render(request, 'register.html', {'form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        
        if register_form.is_valid():
            register_form.save()
            return redirect('/login')
        
        return render(request, 'register.html', {'form': register_form})


class SitterView(View):
    def get(self, request, id):
        sitter = PetSitter.objects.get(pk=id)
        reviews = sitter.reviews.all().order_by('-created_at')[:10]
        request.session['previous_url'] = request.META.get('HTTP_REFERER')
        context = {
            'sitter': sitter,
            'reviews': reviews,
            'avg_rating': sitter.average_rating(),
            'total_reviews': sitter.total_reviews(),
        }
        user_id = request.session.get('user_id')

        if user_id:
            user = User.objects.get(pk=user_id)
            context['user'] = user

        return render(request, 'sitter_detail.html', context)

    def post(self, request):
        return render(request, 'sitter_detail.html')


class BookingFormView(View):
    def get(self, request, sitter_id):
        sitter = PetSitter.objects.get(pk=sitter_id)
        form = BookingForm(sitter=sitter)
        user_id = request.session.get('user_id')
    
        context = {
            'form': form,
            'sitter': sitter,
        }

        if user_id:
            user = User.objects.get(pk=user_id)
            context['user'] = user
        return render(request, 'booking_form.html', context)

    def post(self, request, sitter_id):
        sitter = PetSitter.objects.get(pk=sitter_id)
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = user
            booking.sitter = sitter
            
            hours = Decimal((booking.end_date - booking.start_date).total_seconds()) / Decimal('3600')
            booking.total_price = Decimal(hours) * sitter.hourly_rate_min
            
            booking.save()

            return redirect('booking_detail', booking_id=booking.id)

        context = {
            'form': form,
            'sitter': sitter,
        }

        if user_id:
            user = User.objects.get(pk=user_id)
            context['user'] = user

        return render(request, 'booking_form.html', context)
    

class BookingDetailView(View):
    def get(self, request, booking_id):
        request.session['previous_url'] = request.META.get('HTTP_REFERER')
        booking = Booking.objects.get(pk=booking_id)
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
    
        if booking.customer != user and booking.sitter.user != user:
            return redirect('/home')
        
        context = {
            'booking': booking,
        }

        if user_id:
            context['user'] = user
        
        return render(request, 'booking_detail.html', context)
    

class ReviewCreateView(View):
    def get(self, request, booking_id):
        form = ReviewForm()
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        booking = Booking.objects.get(pk=booking_id, customer=user, status='completed')

        context = {
            'form': form,
            'booking': booking,
        }
        if user_id:
            context['user'] = user

        if hasattr(booking, 'review'):
            return render(request, 'booking_detail.html', context)

        return render(request, 'review_form.html', context)
    
    def post(self, request, booking_id):
        form = ReviewForm(request.POST)
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        booking = Booking.objects.get(pk=booking_id, customer=user, status='completed')

        context = {
            'form': form,
            'booking': booking,
        }
        if user_id:
            context['user'] = user

        if hasattr(booking, 'review'):
            return render(request, 'booking_detail.html', context)

        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.sitter = booking.sitter
            review.customer = user
            review.save()

            return redirect('sitter', id=booking.sitter.id)


def user_bookings(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    bookings_list = Booking.objects.filter(
        customer=user
    ).select_related('sitter__user', 'pet_type').order_by('-created_at')
    
    stats = {
        'total': bookings_list.count(),
        'pending': bookings_list.filter(status='pending').count(),
        'confirmed': bookings_list.filter(status='confirmed').count(),
        'completed': bookings_list.filter(status='completed').count(),
        'cancelled': bookings_list.filter(status='cancelled').count(),
    }
    
    context = {
        'bookings': bookings_list,
        'stats': stats,
        'user': user
    }
    return render(request, 'user_bookings.html', context)


def cancel_booking(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    booking.status = 'cancelled'
    booking.save()

    return redirect('user_bookings')
    # return render(request, 'user_bookings.html', context)