from django.urls import path
from .views import AddtoCardView

urlpatterns = [
    path('product_add/<int:id>', AddtoCardView.as_view(), name='product_card_add')
]