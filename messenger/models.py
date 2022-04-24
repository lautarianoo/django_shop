from django.contrib.auth import get_user_model
from django.db import models
from customer.models import Customer, CompanySeller
from product.models import CustomImage

User = get_user_model()

class Room(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        related_name='rooms',
        blank=True,
        null=True
    )

    company = models.ForeignKey(
        CompanySeller,
        on_delete=models.SET_NULL,
        related_name='rooms',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.customer.user.first_name} {self.customer.user.last_name} | {self.company.title}"

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"

class Message(models.Model):

    author = models.ForeignKey(
        User,
        related_name='messages',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    room = models.ForeignKey(
        Room,
        related_name='messages',
        on_delete=models.CASCADE,
        blank=True
    )
    text = models.TextField(max_length=3500)
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='messages', blank=True, null=True)
    is_company = models.BooleanField(default=False)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room.id}"

    class Meta:
        verbose_name="Сообщение"
        verbose_name_plural="Сообщения"
