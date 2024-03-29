# Generated by Django 3.2.9 on 2022-09-26 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Наименование категории')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение категории')),
                ('slug', models.SlugField(max_length=30, unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Наименование подкатегории')),
                ('slug', models.SlugField(max_length=30, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=55, verbose_name='Наименование товара')),
                ('description', models.TextField(max_length=2000, verbose_name='Описание товара')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('quantity', models.IntegerField(default=0, verbose_name='Количество')),
                ('quantity_sell', models.IntegerField(default=0, verbose_name='Количество проданного')),
                ('available', models.BooleanField(default=False, verbose_name='Есть в наличии')),
                ('date_publication', models.DateTimeField(auto_now_add=True)),
                ('query_product', models.TextField(blank=True, null=True, verbose_name='Запросы продуктов или категории')),
                ('published', models.BooleanField(default=False)),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
                ('sale', models.BooleanField(default=False, verbose_name='Распродажа')),
                ('sale_percent', models.IntegerField(default=0, verbose_name='Скидка')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.category', verbose_name='Категория')),
                ('images', models.ManyToManyField(related_name='product', to='product.ProductImage', verbose_name='Изображения товара')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='company.companyseller', verbose_name='Продавец')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='product.subcategory', verbose_name='Подкатегория'),
        ),
    ]
