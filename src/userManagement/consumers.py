import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Notification
from asgiref.sync import sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
        else:
            self.group_name = f"user_{self.user.id}"
            # Ajouter l'utilisateur à un groupe unique basé sur son ID
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Retirer l'utilisateur du groupe à la déconnexion
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Charger les notifications non lues pour cet utilisateur
        notifications = await self.get_notifications()
        notifications_data = [{"message": n.message, "created_at": n.created_at.strftime('%Y-%m-%d %H:%M:%S')} for n in notifications]

        await self.send(text_data=json.dumps({
            "notifications": notifications_data
        }))

    async def send_notification(self, event):
        # Méthode pour envoyer une notification en temps réel
        notification = event['notification']
        await self.send(text_data=json.dumps({
            "notifications": [notification]
        }))

    @sync_to_async
    def get_notifications(self):
        # Récupérer les notifications non lues de manière synchrone mais l'appeler de manière asynchrone
        return Notification.objects.filter(user=self.user, is_read=False).order_by('-created_at')



