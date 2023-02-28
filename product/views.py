from django.shortcuts import render, redirect
from django.views import View
from src.utils.mixins import CustomerMixin
from .models import SubCategory, Product, Category,Action
import datetime, time

class MainPageView(CustomerMixin, View):

    def get(self, request, *args, **kwargs):
        sub_categories = SubCategory.objects.all()
        actions = Action.objects.filter(is_active=True)
        products = Product.objects.all()
        return render(request, 'product/main_page.html', {'sub_categories': sub_categories, 'products': products})


class SubCategoryDetail(CustomerMixin, View):

    def get(self, request, *args, **kwargs):
        category = SubCategory.objects.filter(id=kwargs.get("id"))[0]
        sub_categories = SubCategory.objects.all()
        return render(request, 'product/detail_subcategory.html', {'sub_categories': sub_categories,'category': category})

class ProductDetail(CustomerMixin, View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(id=kwargs.get("id"))[0]
        return render(request, 'product/detail_product.html',
                      {'product': product})

class CartUserView(CustomerMixin, View):

    def get(self, request, *args, **kwargs):
        cart = request.user.customer.cart
        return render(request, "product/cart.html", {"cart": cart})

class AddCartView(CustomerMixin, View):

    def get(self, request, *args, **kwargs):
        cart = request.user.customer.cart
        product = Product.objects.get(id=kwargs.get("id"))
        cart.products.add(product)
        cart.total_price += product.price
        cart.save()
        return redirect("cart")

class SearchView(View):

    def get(self, request, *args, **kwargs):
        sub_categories = SubCategory.objects.all()
        products = Product.objects.filter(title__icontains=request.GET.get("q"))
        return render(request, 'product/main_page.html', {'sub_categories': sub_categories, 'products': products})