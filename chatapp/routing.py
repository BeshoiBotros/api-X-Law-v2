from django.urls import path
from . import consumers

chat_websockets = [
    path("ws/chat/<int:lawyer_id>/", consumers.ChatConsumer.as_asgi()),
]