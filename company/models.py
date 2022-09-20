import sys
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from customer.models import ShopUser

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
        ShopUser,
        on_delete=models.CASCADE,
        blank=True,
        related_name="company"
    )

    status = models.CharField(
        'Верификация',
        choices=STATUS_COMPANY,
        max_length=30,
        blank=True,
        null=True
    )
    title = models.CharField("Название компании", max_length=50)
    phone = models.CharField("Телефон компании", blank=True, null=True, max_length=16)
    rating_product = models.FloatField("Рейтинг продуктов", default=0.0)
    logo = models.ImageField("Логотип компании", blank=True)
    date_reg = models.DateTimeField(auto_now_add=True)
    premium_seller = models.BooleanField("Премиум продавец", default=False)
    objects = CompanyManager()

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

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
