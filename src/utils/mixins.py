from django.views import View
from customer.models import ShippingAddress
from cart.models import Cart


class CustomerMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            if ShippingAddress.objects.filter(customer=user.customer)[0]:
                address = ShippingAddress.objects.create(customer=user.customer)
                address.save()
            if Cart.objects.filter(customer=user.customer)[0]:
                cart = Cart.objects.create(customer=user.customer)
                cart.save()
        return super().dispatch(request, *args, **kwargs)
