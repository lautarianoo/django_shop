from django.shortcuts import render
from django.views import View
from src.utils.mixins import CustomerMixin
from .models import SubCategory

class MainPageView(CustomerMixin, View):

    def get(self, request, *args, **kwargs):
        sub_categories = SubCategory.objects.all()
        return render(request, 'product/main_page.html', {'sub_categories': sub_categories})
