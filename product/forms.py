from django import forms
from .models import Product, ProductFeature

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'price', 'quantity')

class ProductFeatureForm(forms.ModelForm):

    class Meta:
        model = ProductFeature
        fields = ('feature', 'value')
