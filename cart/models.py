from django.db import models
from product.models import Product
from django.core import checks
from customer.models import Customer

class CartItem(models.Model):

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        blank=True,
        related_name='items',
    )
    quantity = models.IntegerField("Количество", default=1)
    date_add = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField("Окончательная цена", default=0)

    class Meta:
        verbose_name = "Объект корзины"
        verbose_name_plural = "Объекты корзины"

    def save(self, *args, **kwargs):
        for price in range(self.quantity):
            self.total_price += self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Объект корзины | {self.product.title}"

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        allowed_types = ['IntegerField', 'SmallIntegerField', 'PositiveIntegerField',
                         'PositiveSmallIntegerField', 'DecimalField', 'FloatField']
        for field in cls._meta.fields:
            if field.attname == 'quantity':
                if field.get_internal_type() not in allowed_types:
                    msg = "Class `{}.quantity` must be of one of the types: {}."
                    errors.append(checks.Error(msg.format(cls.__name__, allowed_types)))
                break
        else:
            msg = "Class `{}` must implement a field named `quantity`."
            errors.append(checks.Error(msg.format(cls.__name__)))
        return errors

class Cart(models.Model):

    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        blank=True,
        related_name='cart'
    )
    cart_items = models.ManyToManyField(
        CartItem,
        blank=True,
        related_name='cart'
    )
    total_price = models.IntegerField("Тотал прайс корзины", default=0)
    date_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"Корзина {self.customer.user.email}"

    def save(self, *args, **kwargs):
        price = 0
        for item in self.cart_items.all():
            price+=item.total_price
        self.total_price = price
        return super().save(*args, **kwargs)