# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ConversionStatusConsumer(WebsocketConsumer):
    def connect(self):
        # Füge den WebSocket-Kanal zu einer allgemeinen Gruppe hinzu
        async_to_sync(self.channel_layer.group_add)(
            "broadcast",  # Allgemeine Gruppe für alle Verbindungen
            self.channel_name
        )
        self.accept()
        print("WebSocket verbunden")

    def disconnect(self, close_code):
        # Entferne den WebSocket-Kanal aus der allgemeinen Gruppe
        async_to_sync(self.channel_layer.group_discard)(
            "broadcast",
            self.channel_name
        )
        print("WebSocket getrennt")

    def video_status_update(self, event):
        # Nachricht an alle WebSocket-Clients senden
        self.send(text_data=json.dumps({
            'status': event['status'],
            'slug': event['slug'],
        }))
