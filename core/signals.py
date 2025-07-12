from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review, Order
from .mistral import is_bad_review
from .telegram_bot import send_telegram_message
from barbershop.settings import TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID
import asyncio


@receiver(post_save, sender=Review)
def check_review(sender, instance, created, **kwargs):
    # Created - это флаг, который показывает, что запись была создана
    if created:
        # Меняем статус на ai_checked_in_progress
        instance.ai_checked_status = "ai_checked_in_progress"
        instance.save()

        # Отправляем на проверку
        review_text = instance.text
        if is_bad_review(review_text):
            instance.ai_checked_status = "ai_cancelled"
        else:
            instance.ai_checked_status = "ai_checked_true"

        instance.save()


@receiver(post_save, sender=Order)
def telegram_order_notify(sender, instance, created, **kwargs):
    # Created - это флаг, который показывает, что запись была создана
    if created:
        # Формируем сообщение в MD разметке
        message = f"""
** Новый заказ {instance.created_at.strftime('%d.%m.%Y %H:%M')} **
Имя: {instance.name}
Телефон: {instance.phone}
Мастер: {instance.master.last_name}
---
Комментарий: {instance.comment}
---
Админ-панель: http://127.0.0.1:8000/admin/core/order/{instance.id}/change/
#заказ #{instance.master.last_name}
"""
        # Отправляем сообщение в телеграм
        asyncio.run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, message))