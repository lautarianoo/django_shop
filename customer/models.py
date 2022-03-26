from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class CustomerManager(models.Manager):

    def get_queryset(self):
        qs = self._queryset_class(self.model, using=self._db).select_related('user')
        return qs

class Customer(models.Model):

    STATUS_AUTH = (
        (0, "Unrecognized"),
        (1, "Registered"),
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

    object = CustomerManager()

    def __str__(self):
        return self.user.email

    def is_guest(self):
        return self.status == 0

