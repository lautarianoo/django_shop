from django.urls import path
from .views import MainPageView, SubCategoryDetail, ProductDetail, CartUserView, AddCartView, SearchView

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('category/<int:id>', SubCategoryDetail.as_view(), name="category_detail"),
    path('product/<int:id>', ProductDetail.as_view(), name="product_detail"),
    path('cart/', CartUserView.as_view(), name="cart"),
    path('add-cart/<int:id>', AddCartView.as_view(), name="add-cart"),
    path("search/", SearchView.as_view(), name="search")
]