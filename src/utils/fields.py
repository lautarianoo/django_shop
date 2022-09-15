from django.utils.translation import gettext_lazy as _
from django.db import models

class CityField(models.CharField):

    def __init__(self, *args, **kwargs):
        defaults = {
            'verbose_name': "Город",
            'max_length': 25,
            'choices': CITIES,
            'blank': True,
            'null': True
        }
        defaults.update(kwargs)
        super().__init__(*args, **defaults)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs['max_length'] == 3:
            kwargs.pop('max_length')
        if kwargs['choices'] == CITIES:
            kwargs.pop('choices')
        return name, path, args, kwargs

CITIES = [
    ("1", "г. Москва"),
    ("2", "г. Санкт-Петербург"),
    ("3", "г. Новосибирск"),
    ("4", "г. Екатеринбург"),
    ("5", "г. Казан"),
    ("6", "г. Нижний Новгород"),
    ("7", "г. Челябинск	"),
    ("8", "г. Самар	"),
    ("9", "г. Омск"),
    ("10", "г. Ростов-на-Дону"),
    ("11", "г. Уфа"),
    ("12", "г. Красноярск"),
    ("13", "г. Воронеж"),
    ("14", "г. Пермь"),
    ("15", "г. Волгоград"),
    ("16", "г. Краснодар"),
    ("17", "г. Саратов"),
    ("18", "г. Тюмень"),
    ("19", "г. Тольятти"),
    ("20", "г. Ижевск"),
    ("21", "г. Барнаул"),
    ("22", "г. Ульяновск"),
    ("23", "г. Иркутск"),
    ("24", "г. Хабаровск"),
    ("25", "г. Махачкала"),
    ("26", "г. Ярославль"),
    ("27", "г. Оренбург	"),
    ("28", "г. Томск"),
    ("29", "г. Новокузнецк"),
    ("30", "г. Кемерово	"),
]