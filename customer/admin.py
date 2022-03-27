from django.contrib import admin
from .models import Customer, CompanySeller, ShippingAddress

admin.site.register(Customer)
admin.site.register(CompanySeller)
admin.site.register(ShippingAddress)