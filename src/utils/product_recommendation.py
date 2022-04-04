from django.db.models import Q
from product.models import Product, Category

def rec_catalog(customer):
    query_text = str(customer.query_product)
    query = query_text.split()
    filter_products = None
    for q in query:
        filter_products = Product.objects.filter(Q(title__icontains=q) | Q(category__title__icontains=q))\
                                 .distinct().order_by('date_publication')
    return filter_products[:40]