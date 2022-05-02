import base64
import json
from channels.generic.websocket import WebsocketConsumer
import random
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from .models import Room

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer = None
        self.company = None
        self.room = None

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = f'chat_{self.room_id}'
        self.user = self.scope['user']
        self.company = self.scope['company']
        self.room = Room.objects.filter(id=self.room_id)[0]

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_id,
            self.channel_name
        )

        self.accept()

