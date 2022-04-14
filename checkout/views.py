from django.shortcuts import render, redirect
from django.views import View
from .forms import ApplyOrganizationForm
from .models import ApplyOrganization
from src.email import generate_code_email, send_email

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
