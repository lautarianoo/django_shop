from django.views import View
from customer.models import Customer, Cart
from django.contrib.gis.geoip2 import GeoIP2
from src.utils.translation import english_to_russian

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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