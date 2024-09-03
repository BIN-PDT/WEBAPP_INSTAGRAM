from django.urls import path
from .views import *


urlpatterns = [
    path("room/public/", chat_view, name="public-chat"),
    path("room/<group_name>/", chat_view, name="chatroom"),
    path("room/private/<username>/", create_private_chatroom, name="private-chat"),
    path("room/group/create/", groupchat_create_view, name="groupchat-create"),
    path("room/group/edit/<group_name>/", groupchat_edit_view, name="groupchat-edit"),
    path(
        "room/group/delete/<group_name>/",
        groupchat_delete_view,
        name="groupchat-delete",
    ),
    path("room/group/leave/<group_name>/", leave_groupchat, name="groupchat-leave"),
]
