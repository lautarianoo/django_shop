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
                for _ in range(2):
                    product = Product.objects.filter(title__icontains=text).order_by('?')
                    if product not in query:
                        query.append(product[0])
                        query.append(product[1])
                        query.append(product[2])
        else:
            query = Product.objects.all()[:20]
        return render(request, 'product/main_page.html', {'sub_categories': sub_categories, 'rec_product': query[:20]})
