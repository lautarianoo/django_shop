import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()

from customer.models import City
import json

CITIES_NAMES = []

with open('russian-cities.json', 'r', encoding='utf-8') as f:
    text = json.load(f)

for s in text:
    City.objects.create(name=s.get("name")).save()
