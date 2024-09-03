from shortuuid import uuid
from django.db import models
from django.contrib.auth.models import User


class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True, blank=True)
    users_online = models.ManyToManyField(
        User, related_name="online_in_groups", blank=True
    )
    is_private = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name="chat_groups", blank=True)
    # GROUP MODE.
    groupchat_name = models.CharField(max_length=128, null=True, blank=True)
    admin = models.ForeignKey(
        User, null=True, blank=True, related_name="groupchats", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.group_name

    def save(self, *args, **kwargs):
        if not self.group_name:
            self.group_name = uuid()
        super().save(*args, **kwargs)


class GroupMessage(models.Model):
    group = models.ForeignKey(
        ChatGroup, related_name="chat_messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.body:
            return f"{self.author.username} : {self.body}"

    class Meta:
        ordering = ["-created"]
