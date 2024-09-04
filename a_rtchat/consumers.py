import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
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

        author_ids = (
            self.chatroom.chat_messages.all()
            .values_list("author_id", flat=True)
            .distinct()[:30]
        )
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

    def online_status_handler(self, _):
        online_users = self.group.users_online.exclude(id=self.user.id)
        # PUBLIC MODE.
        online_in_public = (
            ChatGroup.objects.get(group_name="public-chat")
            .users_online.exclude(id=self.user.id)
            .exists()
        )
        # PRIVATE MODE.
        online_in_privates = (
            self.user.chat_groups.filter(is_private=True)
            .annotate(
                online_count=Count("users_online", filter=~Q(users_online=self.user))
            )
            .filter(online_count__gt=0)
            .exists()
        )
        # GROUP MODE.
        online_in_groups = (
            self.user.chat_groups.filter(groupchat_name__isnull=False)
            .annotate(
                online_others=Count("users_online", filter=~Q(users_online=self.user))
            )
            .filter(online_others__gt=0)
            .exists()
        )
        # GENERAL.
        online_in_chats = online_in_public or online_in_privates or online_in_groups

        context = {
            "user": self.user,
            "online_users": online_users,
            "online_in_chats": online_in_chats,
            "online_in_public": online_in_public,
        }
        html = render_to_string("a_rtchat/partials/online_status.html", context)
        self.send(text_data=html)
