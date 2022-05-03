import base64
import json
from channels.generic.websocket import WebsocketConsumer
import random
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from .models import Room, Message
from customer.models import Customer, CompanySeller

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer = None
        self.company = None
        self.room = None

    def fetch_messages(self, data):
        messages = Message.objects.filter(room=self.room).order_by('date_add')
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages),
        }
        return self.send_message(content)

    def new_message(self, data):
        author = data['author']
        user = User.objects.filter(id=author)[0]

        if user.company and user.company.is_verify:
            message = Message.objects.create(
                author=user,
                text=data['message'],
                room=self.room
            )
        else:
            message = Message.objects.create(
                author=user,
                text=data['message'],
                room=self.room,
                is_company=True
            )

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }

        return self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

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

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    @staticmethod
    def message_to_json(message):
        return {
            'author': message.author.id,
            'content': message.text,
            'imageurl': message.author.avatar.url,
            'fullname': message.author.full_name,
            'timestamp': str(message.date_add)
        }

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_id,
            self.channel_name
        )

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_id,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        return self.commands[data['command']](self, data)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))