from django.db import models
from src.utils.translate import translation
from customer.models import CompanySeller

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
    quantity = models.IntegerField("Количество", default=0)
    quantity_sell = models.IntegerField("Количество проданного", default=0)
    available = models.BooleanField("Есть в наличии", default=False)

    def check_available(self):
        if self.quantity == self.quantity_sell:
            self.available = False
            return False
        self.available = True
        return True

    def __str__(self):
        return f"{self.title} | {self.company}"