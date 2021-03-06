from django.db import models
from src.utils.translate import translation
from customer.models import CompanySeller
from django.core import checks

class Category(models.Model):

    title = models.CharField("Название категории", max_length=70)
    slug = models.SlugField(max_length=70, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = translation(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class CustomImage(models.Model):

    image = models.ImageField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.slug}"

    class Meta:
        verbose_name="Изображения"
        verbose_name_plural="Изображении"

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
    company = models.ForeignKey(
        CompanySeller,
        on_delete=models.CASCADE,
        related_name="products",
        blank=True
    )
    image = models.ManyToManyField(
        CustomImage,
        blank=True,
        related_name='products'
    )
    price = models.IntegerField("Цена", default=0)
    quantity = models.IntegerField("Количество", default=0)
    quantity_sell = models.IntegerField("Количество проданного", default=0)
    available = models.BooleanField("Есть в наличии", default=False)
    date_publication = models.DateTimeField(auto_now_add=True)
    query_product = models.TextField("Запросы продуктов или категории",
                                     blank=True, null=True)
    published = models.BooleanField(default=False)
    sale_percent = models.IntegerField("Скидка", default=0)
    article = models.IntegerField("Артикль", default=0)

    def check_available(self):
        if self.quantity <= self.quantity_sell:
            self.available = False
            return False
        self.available = True
        return True

    def price_before_sale(self):
        return self.price - (self.price * self.sale_percent)

    def save(self, *args , **kwargs):
        if not self.article:
            self.article = self.id + 1
        return super().save(*args, **kwargs)

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

class CategoryFeature(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='features'
    )
    feature_name = models.CharField("Название характеристики", max_length=100, unique=True)
    unit = models.CharField("Величина", max_length=13, help_text="Например: Герц")

    def __str__(self):
        return f"{self.feature_name} | {self.category.title}"

    class Meta:
        verbose_name = "Характеристика категории"
        verbose_name_plural = "Характеристики категорий"

class ProductFeature(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='features'
    )
    feature = models.ForeignKey(
        CategoryFeature,
        on_delete=models.CASCADE,
        related_name='product_features'
    )
    value = models.CharField("Значение", max_length=30)

    def __str__(self):
        return f"Характеристика {self.product.title}"

    class Meta:
        verbose_name = "Характеристика продукта"
        verbose_name_plural = "Характеристики продуктов"