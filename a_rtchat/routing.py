from django.urls import path
from .consumers import *


websocket_urlpatterns = [
    path("ws/chatroom/<group_name>/", ChatroomConsumer.as_asgi()),
    path("ws/online_status/", OnlineStatusConsumer.as_asgi()),
]
