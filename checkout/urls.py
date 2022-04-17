from django.urls import path
from .views import SendCodeCustomer, VerifyCustomer, VerifyCompany

urlpatterns = [
    path('send_code/', SendCodeCustomer.as_view(), name="send_code"),
    path('verify', VerifyCustomer.as_view(), name="verify_customer"),
    path('verifyc/<int:id>', VerifyCompany.as_view(), name='verify_company')
]