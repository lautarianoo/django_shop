import sys
from io import BytesIO

from PIL import Image
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from src.utils.fields import CityField


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class PountIssue(models.Model):
    '''Адрес пункта выдачи'''

    city = CityField()
    address = models.CharField(verbose_name="Адрес пункта выдачи", max_length=120)
    zip_code = models.CharField(
        "ZIP code",
        max_length=12,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "Адрес выдачи"
        verbose_name_plural = "Адреса выдачи"

    def save(self, *args, **kwargs):
        if not self.address:
            self.address = f"Россия, {self.city}, {self.zip_code}"
        super().save(*args, **kwargs)



class ShopUser(AbstractBaseUser):

    first_name = models.CharField(verbose_name="Имя", max_length=40)
    last_name = models.CharField(verbose_name="Фамилия", max_length=45)
    email = models.EmailField(verbose_name="Почта", unique=True)
    phone = models.CharField(verbose_name="Номер телефона", max_length=10, blank=True, null=True, unique=True)
    date_reg = models.DateTimeField(verbose_name="Дата регистрации", auto_now_add=True)
    avatar = models.ImageField(verbose_name="Аватар")
    status_email = models.BooleanField(default=False)
    city = CityField()
    is_admin = models.BooleanField(default=False)
    full_name = models.CharField(verbose_name="ФИО", max_length=85)

    objects = MyUserManager()

    def __str__(self):
        return self.email

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
        self.full_name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

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
        ShopUser, verbose_name="Юзер",
        on_delete=models.CASCADE,
        related_name="customer"
    )
    status = models.CharField(verbose_name="Статус покупателя", choices=STATUS_AUTH, max_length=20)
    point_issue = models.ForeignKey(
        PountIssue,
        verbose_name="Пункт доставки покупателя",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="customer"
    )
    product_query = models.TextField(verbose_name="Запросы продуктов", max_length=5000)

    class Meta:
        verbose_name='Покупатель'
        verbose_name_plural='Покупатели'

    object = CustomerManager()

    def __str__(self):
        return self.user.email

    def is_guest(self):
        return self.status == 0
