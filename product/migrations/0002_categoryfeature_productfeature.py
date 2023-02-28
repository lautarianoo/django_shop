# Generated by Django 3.2.9 on 2022-09-27 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='Наименование характеристики')),
                ('value', models.CharField(max_length=30, verbose_name='Значение')),
                ('unit', models.CharField(max_length=10, verbose_name='Единица измерение (Гц, кг и т.д.)')),
                ('products', models.ManyToManyField(blank=True, related_name='feature', to='product.Product', verbose_name='Продукт(ы)')),
            ],
            options={
                'verbose_name': 'Характиерстика продукта',
                'verbose_name_plural': 'Характеристики продуктов',
            },
        ),
        migrations.CreateModel(
            name='CategoryFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='Наименование характеристики')),
                ('value', models.CharField(max_length=30, verbose_name='Значение')),
                ('unit', models.CharField(max_length=10, verbose_name='Единица измерение (Гц, кг и т.д.)')),
                ('categories', models.ManyToManyField(blank=True, related_name='feature', to='product.Category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Характиерстика категорий',
                'verbose_name_plural': 'Характеристики категорий',
            },
        ),
    ]
