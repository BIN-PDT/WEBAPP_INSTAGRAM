from uuid import uuid4
from django.db import models


class Post(models.Model):
    id = models.CharField(
        max_length=100, primary_key=True, editable=False, default=uuid4
    )
    title = models.CharField(max_length=500)
    image = models.URLField(max_length=500)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ["-created"]
