# Generated by Django 3.2.9 on 2022-12-03 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_action_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активная акция'),
        ),
    ]
