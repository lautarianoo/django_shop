from django.shortcuts import redirect
from django.views import View
from customer.models import ShippingAddress
from cart.models import Cart
from customer.models import CompanySeller

class CustomerMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            if not ShippingAddress.objects.filter(customer=user.customer)[0]:
                address = ShippingAddress.objects.create(customer=user.customer)
                address.save()
            if not Cart.objects.filter(customer=user.customer)[0]:
                cart = Cart.objects.create(customer=user.customer)
                cart.save()
        return super().dispatch(request, *args, **kwargs)

class CompanyMixin(View):

    def dispatch(self, request, *args, **kwargs):
        company = request.user.company
        if company.STATUS_COMPANY != "Verify":
            return redirect('catalog')
        return super().dispatch(request, *args, **kwargs)
