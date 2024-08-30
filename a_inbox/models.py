from uuid import uuid4
from django.utils import timezone
from django.utils.timesince import timesince
from django.db import models
from django.contrib.auth.models import User


class InboxMessage(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    conversation = models.ForeignKey(
        "Conversation", on_delete=models.CASCADE, related_name="messages"
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        time_since = timesince(self.created, timezone.now())
        return f"[{self.sender.username} : {time_since} ago]"

    class Meta:
        ordering = ["-created"]


class Conversation(models.Model):
    id = models.CharField(
        max_length=100, primary_key=True, editable=False, default=uuid4
    )
    participants = models.ManyToManyField(User, related_name="conversations")
    lastmessage_created = models.DateTimeField(default=timezone.now)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        user_names = ", ".join(user.username for user in self.participants.all())
        return f"[{user_names}]"

    class Meta:
        ordering = ["-lastmessage_created"]
