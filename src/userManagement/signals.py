from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from userManagement.models import Notification
from django.db.models.signals import post_save

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        # Diffuser la notification à l'utilisateur concerné
        channel_layer = get_channel_layer()
        group_name = f"user_{instance.user.id}"
        notification_data = {
            "message": instance.message,
            "created_at": instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "notification": notification_data
            }
        )
