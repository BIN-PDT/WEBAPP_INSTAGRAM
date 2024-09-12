from django.urls import path
from .views import *


urlpatterns = [
    path("public/", chat_view, name="public-chat"),
    path("room/<group_name>/", chat_view, name="chatroom"),
    path("private/<username>/", create_private_chatroom, name="private-chat"),
    path("group/create/", groupchat_create_view, name="groupchat-create"),
    path("group/edit/<group_name>/", groupchat_edit_view, name="groupchat-edit"),
    path("group/delete/<group_name>/", groupchat_delete_view, name="groupchat-delete"),
    path("group/leave/<group_name>/", leave_groupchat, name="groupchat-leave"),
    path("room/file_upload/<group_name>/", chat_file_upload, name="chat-file-upload"),
    path("check_member/<group_name>/", check_member),
]
