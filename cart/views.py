from django.shortcuts import render, redirect
from .models import Cart, CartItem
from django.views import View
from product.models import Product

class AddtoCardView(View):

    def post(self, request, *args, **kwargs):
        product = Product.objects.filter(id=kwargs.get('id'))[0]
        cart_item = CartItem.objects.create(product=product, total_price=product.price)
        cart_item.save()
        request.user.customer.cart.cart_items.add(cart_item)
        request.user.customer.cart.save()
        return redirect('catalog')
