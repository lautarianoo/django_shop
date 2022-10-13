from django.shortcuts import render
from django.views import View
from src.utils.mixins import CustomerMixin
from .models import SubCategory, Product

class MainPageView(CustomerMixin, View):

    def get(self, request, *args, **kwargs):
        sub_categories = SubCategory.objects.all()
        if request.user.is_authenticated and request.user.customer.product_query:
            query = []
            for text in request.user.customer.product_query.split(" "):
                for _ in range(2):
                    product = Product.objects.filter(title__icontains=text).order_by('?')
                    if product:
                        if product[0] not in query and product[1] not in query and product[2] not in query:
                            query.append(product[0])
                            query.append(product[1])
                            query.append(product[2])
        else:
            query = Product.objects.filter(tezone_recommended=True)[:50]
        return render(request, 'product/main_page.html', {'sub_categories': sub_categories, 'rec_product': query[:40]})
