import base64
import json
from channels.generic.websocket import WebsocketConsumer
import random
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    pass