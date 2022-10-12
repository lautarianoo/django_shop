from django.views import View
from customer.models import Customer

class CustomerMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not Customer.objects.filter(user=request.user):
                new_customer = Customer.objects.create(user=request.user, status=1)
                new_customer.save()
        return super().dispatch(request, *args, **kwargs)