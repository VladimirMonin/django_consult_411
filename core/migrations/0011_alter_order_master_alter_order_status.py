# Generated by Django 5.2.1 on 2025-06-28 07:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_order_created_at_order_status_order_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='master',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='orders', to='core.master', verbose_name='Мастер'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('new', 'Новая'), ('confirmed', 'Подтверждена'), ('completed', 'Выполнена'), ('cancelled', 'Отменена')], default='new', max_length=20, null=True, verbose_name='Статус'),
        ),
    ]
