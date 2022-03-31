from django.db import models
from src.utils.translate import translation
from customer.models import CompanySeller
from django.core import checks

class Category(models.Model):

    title = models.CharField("Название категории", max_length=70)
    slug = models.SlugField(max_length=70)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = translation(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='products'
    )
    title = models.CharField("Название продукта", max_length=300)
    description = models.TextField("Описание", max_length=2000)
    company = models.ForeignKey(CompanySeller, on_delete=models.CASCADE, related_name="products")
    price = models.IntegerField("Цена", default=0)
    quantity = models.IntegerField("Количество", default=0)
    quantity_sell = models.IntegerField("Количество проданного", default=0)
    available = models.BooleanField("Есть в наличии", default=False)

    def check_available(self):
        if self.quantity <= self.quantity_sell:
            self.available = False
            return False
        self.available = True
        return True

    def __str__(self):
        return f"{self.title} | {self.company}"

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