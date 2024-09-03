import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from .models import *


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.group_name)

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        # UPDATE ONLINE COUNT.
        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()

        self.accept()

    def disconnect(self, _):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        # UPDATE ONLINE COUNT.
        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json["body"]

        message = GroupMessage.objects.create(
            body=message_content, author=self.user, group=self.chatroom
        )

        event = {"type": "message_handler", "message_id": message.id}
        async_to_sync(self.channel_layer.group_send)(self.group_name, event)

    def message_handler(self, event):
        message_id = event["message_id"]
        message = GroupMessage.objects.get(id=message_id)

        context = {"user": self.user, "message": message}
        html = render_to_string("a_rtchat/partials/chat_message.html", context)
        self.send(text_data=html)

    def update_online_count(self):
        online_count = self.chatroom.users_online.count() - 1

        event = {"type": "online_count_handler", "online_count": online_count}
        async_to_sync(self.channel_layer.group_send)(self.group_name, event)

    def online_count_handler(self, event):
        online_count = event["online_count"]

        context = {"online_count": online_count, "chatroom": self.chatroom}
        html = render_to_string("a_rtchat/partials/online_count.html", context)
        self.send(text_data=html)
