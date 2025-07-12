from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
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


@receiver(m2m_changed, sender=Order.services.through)
def telegram_order_notify(sender, instance, action, **kwargs):
    """
    Обработчик сигнала m2m_changed для модели Order.
    Отправляет уведомление только при создании НОВОГО заказа с услугами.
    """
    # action == 'post_add' - означает, что в M2M-связь добавили записи.
    # pk_set - содержит id добавленных услуг.
    # Проверяем, что заказ был создан менее 5 секунд назад.
    # Это позволяет отфильтровать именно создание нового заказа, а не обновление старого.
    if action == 'post_add' and kwargs.get('pk_set') and timezone.now() - instance.created_at < timedelta(seconds=5):
        # Получаем список услуг
        services = [service.name for service in instance.services.all()]

        # Формируем сообщение в MD разметке
        message = (
            f"**Новый заказ {instance.created_at.strftime('%d.%m.%Y %H:%M')}**\n"
            f"Имя: {instance.name}\n"
            f"Телефон: {instance.phone}\n"
            f"Мастер: {instance.master.last_name}\n"
            f"Услуги: {', '.join(services) or 'Не указано'}\n"
            "---\n"
            f"Комментарий: {instance.comment or 'Не указан'}\n"
            f"#заказ #{instance.master.last_name}"
        )
        # Отправляем сообщение в телеграм
        asyncio.run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, message))