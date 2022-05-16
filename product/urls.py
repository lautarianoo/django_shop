from django.urls import path
from .views import CatalogView, AddFeatureProduct

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('add_feature/', AddFeatureProduct.as_view(), name='add_feature')
]