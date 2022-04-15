from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from cart.models import Cart
from django.views import View
from .forms import LoginForm, RegistrationForm, CreateCompanyForm
from customer.models import Customer, ShippingAddress
from src.utils.mixins import CustomerMixin
from checkout.models import ApplyOrganization

class LoginView(CustomerMixin, View):

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
        form = RegistrationForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            customer = Customer.objects.create(user=new_user, status="Unrecognized")
            customer.save()
            cart = Cart.objects.create(customer=customer)
            cart.save()
            address = ShippingAddress.objects.create(customer=customer)
            address.save()
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            return redirect('login')
        return render(request, 'customer/register.html', {'form': form})

class CreateCompany(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.STATUS_AUTH == "Recognized":
            form = CreateCompanyForm()
            return render(request, 'customer/create_company.html', {'form': form})
        return redirect('catalog')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.STATUS_AUTH == "Recognized":
            form = CreateCompanyForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                new_company = form.save(commit=False)
                new_company.STATUS_COMPANY = "No verify"
                new_company.user = request.user
                new_company.save()
                return redirect('catalog')
            return render(request, 'customer/register.html', {'form': form})
