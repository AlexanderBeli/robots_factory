from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from robots.models import Robot

ROBOT_AVAILABLE_MESSAGE_TEMPLATE = """
Добрый день!
Недавно вы интересовались нашим роботом модели {model}, версии {version}.
Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.
"""


@receiver(post_save, sender=Robot)
def robot_available_mail(sender, instance, created, **kwargs):
    if created:
        subject = "Уведомление о статусе заказа"
        model = instance.version.model.model
        version = instance.version.version
        message = ROBOT_AVAILABLE_MESSAGE_TEMPLATE.format(model=model, version=version)
        recipients = [
            "example@example.com",
        ]
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.ADMIN_EMAIL,
            recipient_list=recipients,
        )
