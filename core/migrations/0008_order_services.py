# Generated by Django 5.2.1 on 2025-06-15 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='services',
            field=models.ManyToManyField(related_name='orders', to='core.service', verbose_name='Услуги'),
        ),
    ]
