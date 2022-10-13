from django.utils.translation import gettext_lazy as _
from django.db import models
import json

class CityField(models.CharField):

    def __init__(self, *args, **kwargs):
        defaults = {
            'verbose_name': "Город",
            'max_length': 25,
            'choices': [],
            'blank': True,
            'null': True
        }
        defaults.update(kwargs)
        super().__init__(*args, **defaults)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs['max_length'] == 3:
            kwargs.pop('max_length')
        if kwargs['choices'] == []:
            kwargs.pop('choices')
        return name, path, args, kwargs

