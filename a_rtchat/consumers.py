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
        if not self.chatroom.users_online.contains(self.user):
            self.chatroom.users_online.add(self.user)
            self.update_online_count()

        self.accept()

    def disconnect(self, _):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        # UPDATE ONLINE COUNT.
        if self.chatroom.users_online.contains(self.user):
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

        context = {
            "user": self.user,
            "message": message,
            "chatroom": self.chatroom,
        }
        html = render_to_string("a_rtchat/partials/chat_message.html", context)
        self.send(text_data=html)

    def update_online_count(self):
        online_count = self.chatroom.users_online.count() - 1

        event = {"type": "online_count_handler", "online_count": online_count}
        async_to_sync(self.channel_layer.group_send)(self.group_name, event)

    def online_count_handler(self, event):
        online_count = event["online_count"]

        chat_messages = ChatGroup.objects.get(
            group_name=self.group_name
        ).chat_messages.all()[:30]
        author_ids = set([message.author.id for message in chat_messages])
        users = User.objects.filter(id__in=author_ids)

        context = {
            "online_count": online_count,
            "chatroom": self.chatroom,
            "users": users,
        }
        html = render_to_string("a_rtchat/partials/online_count.html", context)
        self.send(text_data=html)


class OnlineStatusConsumer(WebsocketConsumer):
    connections = []

    def connect(self):
        self.user = self.scope["user"]
        self.connections.append(self.user.id)
        self.group_name = "online-status"
        self.group = get_object_or_404(ChatGroup, group_name=self.group_name)

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        if not self.group.users_online.contains(self.user):
            self.group.users_online.add(self.user)

        self.accept()
        self.online_status()

    def disconnect(self, _):
        self.connections.remove(self.user.id)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        if self.connections.count(
            self.user.id
        ) == 0 and self.group.users_online.contains(self.user):
            self.group.users_online.remove(self.user)

        self.online_status()

    def online_status(self):
        event = {"type": "online_status_handler"}
        async_to_sync(self.channel_layer.group_send)(self.group_name, event)

    def online_status_handler(self, event):
        online_users = self.group.users_online.exclude(id=self.user.id)
        # PUBLIC MODE.
        public_chat_users = ChatGroup.objects.get(
            group_name="public-chat"
        ).users_online.exclude(id=self.user.id)
        # PRIVATE MODE.
        private_chats_with_users = [
            chat
            for chat in self.user.chat_groups.filter(is_private=True)
            if chat.users_online.exclude(id=self.user.id).exists()
        ]
        # GROUP MODE.
        group_chats_with_users = [
            chat
            for chat in self.user.chat_groups.filter(groupchat_name__isnull=False)
            if chat.users_online.exclude(id=self.user.id).exists()
        ]

        online_in_chats = (
            public_chat_users.exists()
            or private_chats_with_users
            or group_chats_with_users
        )

        context = {
            "user": self.user,
            "online_users": online_users,
            "online_in_chats": online_in_chats,
            "public_chat_users": public_chat_users,
        }
        html = render_to_string("a_rtchat/partials/online_status.html", context)
        self.send(text_data=html)
