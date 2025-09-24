from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q

from .forms import *

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
        return redirect('/home')


def home(request):
    pet_types = PetType.objects.all()
    sitters = PetSitter.objects.all()

    search_query = request.GET.get('search', '')
    pet_type = request.GET.get('pet_type', '')
    location = request.GET.get('location', '')

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