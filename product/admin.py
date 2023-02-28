from django.contrib import admin
from .models import SubCategory, Category, CategoryFeature, ProductFeature, Product, ProductImage, Action

admin.site.register(SubCategory)
admin.site.register(CategoryFeature)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Product)
admin.site.register(ProductFeature)
admin.site.register(Action)
