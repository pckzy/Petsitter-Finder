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
        request.session['previous_url'] = request.META.get('HTTP_REFERER')
        context = {
            'sitter': sitter
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
    