from uuid import uuid4
from django.db import models


class Post(models.Model):
    id = models.CharField(
        max_length=100, primary_key=True, editable=False, default=uuid4
    )
    url = models.URLField(max_length=500, null=True)
    artist = models.CharField(max_length=500, null=True)
    title = models.CharField(max_length=500)
    image = models.URLField(max_length=500)
    body = models.TextField()
    tags = models.ManyToManyField("Tag")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ["-created"]


class Tag(models.Model):
    image = models.FileField(upload_to="icons/", null=True, blank=True)
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ["order"]
