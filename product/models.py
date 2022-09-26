from django.db import models
from company.models import CompanySeller
from src.utils.translation import russian_to_engilsh


class SubCategory(models.Model):

    name = models.CharField("Наименование подкатегории", max_length=30)
    slug = models.SlugField("Слаг", max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Подкатегория"
        verbose_name_plural = "Подкатегории"

class Category(models.Model):

    name = models.CharField("Наименование категории", max_length=30)
    image = models.ImageField(verbose_name="Изображение категории")
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name="Подкатегория",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="categories"
    )
    slug = models.SlugField("Слаг", max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class ProductImage(models.Model):

    image = models.ImageField(verbose_name="Изображение")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.slug}"

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

class Product(models.Model):

    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )
    seller = models.ForeignKey(
        CompanySeller,
        verbose_name="Продавец",
        on_delete=models.CASCADE,
        related_name="products"
    )
    images = models.ManyToManyField(ProductImage, verbose_name="Изображения товара", related_name="product")
    title = models.CharField("Наименование товара", max_length=55)
    description = models.TextField(verbose_name="Описание товара", max_length=2000)
    price = models.IntegerField(verbose_name="Цена")
    quantity = models.IntegerField("Количество", default=0)
    quantity_sell = models.IntegerField("Количество проданного", default=0)
    available = models.BooleanField("Есть в наличии", default=False)
    date_publication = models.DateTimeField(auto_now_add=True)
    query_product = models.TextField("Запросы продуктов или категории",
                                     blank=True, null=True)
    published = models.BooleanField(default=False)
    slug = models.SlugField(verbose_name="Слаг", unique=True)
    sale=models.BooleanField(verbose_name="Распродажа", default=False)
    sale_percent = models.IntegerField("Скидка", default=0)

    def __str__(self):
        return f"{self.category.name} | {self.title} | {self.seller.title}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def save(self, *args, **kwargs):
        if self.sale:
            self.price = self.price * (self.sale_percent / 100)
        if self.quantity == self.quantity_sell or self.quantity == 0:
            self.available = False
        self.slug = f"{russian_to_engilsh(self.title)}-{self.id}"
        super().save(*args, *kwargs)