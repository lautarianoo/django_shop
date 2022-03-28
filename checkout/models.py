from django.db import models
from customer.models import CompanySeller

class ApplyOrganization(models.Model):

    CATEGORY_ORGANIZATION = (
        (0, "ИП"),
        (1, "ООО")
    )

    company = models.ForeignKey(CompanySeller, on_delete=models.CASCADE, related_name='applications')
    name_organization = models.CharField("Название организации", max_length=80)
    number_inn = models.CharField("Регистрационный номер организации", max_length=30)
    address = models.CharField("Адрес организации", max_length=80)
    phone = models.CharField("Номер организации", max_length=18)
    accepted = models.BooleanField("Заявка принята", default=False)
    no_accepted = models.BooleanField("Заявка отклонена", default=False)

    def __str__(self):
        return f"{self.company.title} | {self.name_organization}"

    class Meta:
        verbose_name = "Заявка на верификацию организации"
        verbose_name_plural = "Заявки на верификацию организации"
