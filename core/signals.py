from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from .mistral import is_bad_review


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
