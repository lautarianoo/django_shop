from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from cart.models import Cart
from django.views import View
from .forms import LoginForm, RegistrationForm

class LoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('catalog')
        form = LoginForm()
        return render(request, 'customer/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('catalog')
        return render(request, 'customer/login.html', {'form': form})

class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('catalog')
        form = RegistrationForm()
        return render(request, 'customer/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        pass