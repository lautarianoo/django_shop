import sys
from io import BytesIO

from PIL import Image
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from src.utils.fields import CountryField

User = get_user_model()

class CustomerManager(models.Manager):

    def get_queryset(self):
        qs = self._queryset_class(self.model, using=self._db).select_related('user')
        return qs

    def create(self, *args, **kwargs):
        if 'user' in kwargs and kwargs['user'].is_authenticated:
            kwargs.setdefault('status', 'Recognized')
        customer = super().create(*args, **kwargs)
        return customer

class Customer(models.Model):

    STATUS_AUTH = (
        (0, "Unrecognized"),
        (1, "Recognized"),
        (2, "Is staff"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name="customer"
    )
    status = models.CharField(
        'Recognized as',
        choices=STATUS_AUTH,
        max_length=30,
        blank=True,
        null=True
    )
    last_action = models.DateTimeField(
        default=timezone.now
    )
    class Meta:
        verbose_name='Покупатель'
        verbose_name_plural='Покупатели'

    object = CustomerManager()

    def __str__(self):
        return self.user.email

    def is_guest(self):
        return self.status == 0

class CompanyManager(models.Manager):

    def get_queryset(self):
        qs = self._queryset_class(self.model, using=self._db).select_related('user')
        return qs

class CompanySeller(models.Model):

    STATUS_COMPANY = (
        (0, "No verify"),
        (1, "Verify"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name="company"
    )

    status = models.CharField(
        'Recognized as',
        choices=STATUS_COMPANY,
        max_length=30,
        blank=True,
        null=True
    )
    title = models.CharField("Название компании", max_length=50)
    phone = models.CharField("Телефон компании", blank=True, null=True, max_length=16)
    logo = models.ImageField("Логотип компании", blank=True)
    date_reg = models.DateTimeField(auto_now_add=True)
    objects = CompanyManager()

    class Meta:
        verbose_name='Компания'
        verbose_name_plural='Компании'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.avatar:
            image = self.avatar
            img = Image.open(image)
            new_img = img.convert('RGB')
            resized_new_img = new_img.resize((200, 200), Image.ANTIALIAS)
            filestream = BytesIO()
            resized_new_img.save(filestream, 'JPEG', quality=90)
            filestream.seek(0)
            name = '{}.{}'.format(*self.avatar.name.split('.'))
            self.avatar = InMemoryUploadedFile(
                filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
            )
        super().save(*args, **kwargs)

    @property
    def is_verify(self):
        return self.status == 1

class ShippingAddress(models.Model):

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="address")
    address1 = models.CharField("Address line 1", max_length=1024, blank=True, null=True)
    address2 = models.CharField("Address line 2", max_length=1024,blank=True,null=True,)
    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )
    city = models.CharField(
        "City",
        max_length=1024,
    )
    country = CountryField("Country")

    class Meta:
        verbose_name="Адрес доставки"
        verbose_name_plural="Адреса доставки"

    def __str__(self):
        return f"{self.customer.email} | {self.zip_code}"

    def save(self, *args, **kwargs):
        if not self.address1:
            self.address1 = f"{self.country}, {self.city}, {self.zip_code}"
        super().save(*args, **kwargs)

class VisitingCustomer:

    user = AnonymousUser()

    def __str__(self):
        return 'Visitor'

    @property
    def email(self):
        return ''

    @email.setter
    def email(self, value):
        pass

    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return False

    @property
    def is_recognized(self):
        return False

    @property
    def is_guest(self):
        return False

    @property
    def is_registered(self):
        return False

    @property
    def is_visitor(self):
        return True
