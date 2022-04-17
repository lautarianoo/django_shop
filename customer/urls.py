from django.urls import path
from .views import LoginView, RegistrationView, CreateCompany

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegistrationView.as_view(), name='register'),
    path('ccompany/', CreateCompany.as_view(), name='create_company')
]