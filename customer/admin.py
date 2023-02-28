from django.contrib import admin
from .models import ShopUser, PountIssue, Customer, City, Cart

admin.site.register(ShopUser)
admin.site.register(PountIssue)
admin.site.register(Customer)
admin.site.register(City)

admin.site.register(Cart)


# Register your models here.
