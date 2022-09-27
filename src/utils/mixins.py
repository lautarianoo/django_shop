from django.views import View
from customer.models import Customer

class CustomerMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.сustomer:
                new_customer = Customer.object.create(user=request.user, status=1)
                new_customer.save()
        return super().dispatch(request, *args, **kwargs)