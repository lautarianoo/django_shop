from django.views import View
from customer.models import Customer, Cart


class CustomerMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not Customer.objects.filter(user=request.user):
                new_customer = Customer.objects.create(user=request.user, status=1)
                new_customer.save()
            if not Cart.objects.filter(customer=request.user.customer):
                new_cart = Cart.objects.create(customer=Customer.objects.filter(user=request.user)[0])
                new_cart.save()
        return super().dispatch(request, *args, **kwargs)