from django.urls import path
from .views import CatalogView

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
]