from django.urls import path
from .views import *


urlpatterns = [
    path("room/public/", chat_view, name="chat"),
    path("room/<chatroom_name>/", chat_view, name="chatroom"),
    path("<username>/", get_or_create_chatroom, name="start-chat"),
]
