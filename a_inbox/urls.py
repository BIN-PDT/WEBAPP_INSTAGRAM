from django.urls import path
from .views import *


urlpatterns = [
    path("", inbox_view, name="inbox"),
    path("conversation/<conversation_id>/", inbox_view, name="inbox"),
    path("search_users/", search_users, name="search-users"),
    path("new_message/<recipient_id>/", new_message, name="new-message"),
    path("new_reply/<conversation_id>/", new_reply, name="new-reply"),
    path("notify/<conversation_id>/", notify_message, name="notify-message"),
    path("notify_inbox/", notify_inbox, name="notify-inbox"),
]
