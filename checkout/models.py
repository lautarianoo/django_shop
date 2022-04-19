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
    category = models.CharField(choices=CATEGORY_ORGANIZATION, max_length=18)
    date_publish = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField("Заявка принята", default=False)
    admin_text = models.TextField("Сообщение принятия/отклонения заявки", max_length=2000,
                                  blank=True, null=True)
    no_accepted = models.BooleanField("Заявка отклонена", default=False)

    def __str__(self):
        return f"{self.company.title} | {self.name_organization}"

    def save(self, *args, **kwargs):
        if self.accepted:
            self.company.status = "Verify"
            self.company.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Заявка на верификацию организации"
        verbose_name_plural = "Заявки на верификацию организации"
