from django.shortcuts import render
from django.views import View

from .forms import *

# Create your views here.
def test(request):
    render(request, 'base.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'base.html')

    def post(self, request):
        return render(request, 'base.html')
