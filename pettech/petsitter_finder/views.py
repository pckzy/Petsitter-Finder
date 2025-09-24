from django.shortcuts import render, redirect
from django.views import View

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
    is_login = request.session.get('user_id')
    if is_login:
        user = User.objects.get(pk=is_login)
        return render(request, 'home.html', {'is_login': is_login, 'user': user})

    return render(request, 'home.html', {'is_login': is_login})


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