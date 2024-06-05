import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from users import models
from XLaw import shortcuts
from . import models as chat_models

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        lawyer_id = self.scope['url_route']['kwargs']['lawyer_id']
        if self.scope.get('user'):
            user_id = self.scope.get('user')['user_id']
            user = shortcuts.object_is_exist_for_sockets(user_id, models.CustomUser, self.send_error_message, "Authentication credentials were not provided.")
            self.user = user
        else:
            self.close()
            return

        lawyer = shortcuts.object_is_exist_for_sockets(lawyer_id, models.CustomUser, self.send_error_message, "user not found")
        
        if lawyer.is_staff:
            self.send_error_message("only users such as lawyers, clients can chat them")
            self.close()
            return
        
        if lawyer:
            room_name = sorted([lawyer.pk, user.pk])
            self.chat_room, _ = chat_models.ChatRoom.objects.get_or_create(name=f'chat_{room_name[0]}_{room_name[1]}')
            self.chat_room.users.add(lawyer, user)
            self.room_group_name = self.chat_room.name
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
        
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )
    
    def send_error_message(self, error_message):
        self.send(text_data=json.dumps({
            'type': 'error',
            'message': error_message
        }))

    def chat_message(self, event):
        message = event["message"]
        chat_models.Message.objects.create(sender=self.user, content=message, chat_room=self.chat_room)
        self.send(text_data=json.dumps({"type" : "chat.message","message": message}))