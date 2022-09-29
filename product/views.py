from django.shortcuts import render
from django.views import View
from src.utils.mixins import CustomerMixin
from .models import SubCategory, Product

class MainPageView(CustomerMixin, View):

    def get(self, request, *args, **kwargs):
        sub_categories = SubCategory.objects.all()
        if request.user.is_authenticated and request.user.query_product:
            query = []
            for text in request.user.query_product.split(" "):
                product = Product.objects.filter(title__icontains=text).order_by('?')[0]
                if product not in query:
                    query.append(product)
        else:
            query = Product.objects.all()[:15]
        return render(request, 'product/main_page.html', {'sub_categories': sub_categories, 'rec_product': query})
