from django.shortcuts import render, redirect
from django.views import View
from customer.models import Customer
from .models import Category, Product
from src.utils.product_recommendation import rec_catalog
from src.utils.mixins import CompanyMixin
from .forms import ProductForm, ProductFeatureForm

class CatalogView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user)[0]
            qs = rec_catalog(customer)
        else:
            qs = Product.objects.all()[:40]
        categories = Category.objects.all()[:5]
        return render(request, 'product/catalog.html', {'products': qs, 'categories': categories})

class CreateProduct(CompanyMixin, View):

    def get(self, request, *args, **kwargs):
        company = request.user.company
        form = ProductForm()
        return render(request, 'product/create_product.html', {'form': form, 'company': company})

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST or None, request.FILES or None)
        company = request.user.company
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.company = company
            new_product.save()
            return redirect('catalog')
        return render(request, 'product/create_product.html', {'form': form, 'company': company})

class AddFeatureProduct(CompanyMixin, View):

    def get(self, request, *args, **kwargs):
        form = ProductFeatureForm()
        return render(request, 'product/product_feature.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if Product.objects.filter(id=kwargs.get('id')) == request.user.company:
            form = ProductFeatureForm(request.POST or None)
            if form.is_valid():
                form.save()
                return redirect('catalog')
            return render(request, 'product/create_product.html', {'form': form})
        return render(request, 'product/create_product.html', {})