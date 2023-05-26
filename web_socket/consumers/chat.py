# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from user.models import User




class ChatConsumer(WebsocketConsumer):
    
    def get_thread_name(self, logged_user_id, other_user_id):
        logged_user_id_is_bigger = logged_user_id > other_user_id
        if logged_user_id_is_bigger:
            thread_name = f'chat_{logged_user_id}-{other_user_id}'
        else:
            thread_name = thread_name = f'chat_{other_user_id}-{logged_user_id}'
        return thread_name
    
    
    def connect(self):
        logged_user = self.scope['user'].id
        other_user = User.objects.get(id=self.scope["url_route"]["kwargs"]["other_user_id"])
        thread_name = self.get_thread_name(logged_user.id,other_user.id)
        self.room_name = thread_name
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
