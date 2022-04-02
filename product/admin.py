from django.contrib import admin
from .models import Category, Product, CategoryFeature, ProductFeature

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CategoryFeature)
admin.site.register(ProductFeature)
