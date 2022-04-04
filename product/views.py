from django.shortcuts import render
from django.views import View
from customer.models import Customer, VisitingCustomer
from .models import Category, Product
from src.utils.product_recommendation import rec_catalog

class CatalogView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user)[0]
            qs = rec_catalog(customer)
        else:
            qs = Product.objects.all()[40]
        categories = Category.objects.all()
        return render(request, 'product/catalog.html', {'products': qs, 'categories': categories})