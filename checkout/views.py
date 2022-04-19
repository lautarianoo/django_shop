from django.shortcuts import render, redirect
from django.views import View
from .forms import ApplyOrganizationForm, AdminEditApplicationForm
from .models import ApplyOrganization
from src.email import generate_code_email, send_email
from customer.models import CompanySeller

class SendCodeCustomer(View):

    def get(self, request, *args, **kwargs):
        code = generate_code_email()
        request.session['code'] = code
        send_email(request.user.email, code)
        return redirect('verify_customer')

class VerifyCustomer(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'checkout/accept_email.html', {})

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.STATUS_AUTH == "Unrecognized":
            if request.POST.get('code') == request.session['code']:
                user.STATUS_AUTH = "Recognized"
                user.save()
        return redirect('catalog')

class VerifyCompany(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.STATUS_AUTH == "Recognized":
            form = ApplyOrganizationForm()
            applications = ApplyOrganization.objects.filter(company=CompanySeller.objects.filter(id=kwargs.get('id'))[0])
            return render(request, 'checkout/verify_company.html', {'form': form, 'applications': applications})
        return redirect('catalog')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.STATUS_AUTH == "Recognized":
            form = ApplyOrganizationForm(request.POST)
            if form.is_valid():
                new_application = form.save(commit=False)
                new_application.company = CompanySeller.objects.filter(id=kwargs.get('id'))[0]
                new_application.save()
                return redirect('catalog')
            applications = ApplyOrganization.objects.filter(
                company=CompanySeller.objects.filter(id=kwargs.get('id'))[0])
            return render(request, 'checkout/verify_company.html', {'form': form, 'applications': applications})
        return redirect('catalog')

class AdminEditApplication(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            form = AdminEditApplicationForm()
            application = ApplyOrganization.objects.filter(id=kwargs.get('id'))
            return render(request, 'checkout/edit_application.html', {'form': form, "application": application})