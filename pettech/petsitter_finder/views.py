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

def home(request):
    return render(request, 'home.html')