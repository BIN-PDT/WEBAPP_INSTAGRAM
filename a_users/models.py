from allauth.account.models import EmailAddress
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.templatetags.static import static


class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        user = super().create_superuser(username, email, password, **extra_fields)
        EmailAddress.objects.create(
            user=user, email=user.email, primary=True, verified=True
        )
        return user


class User(AbstractUser):
    objects = CustomUserManager()

    def __str__(self):
        return str(self.username)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="avatars/", null=True, blank=True)
    realname = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    location = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    @property
    def name(self):
        return self.realname if self.realname else self.user.username

    @property
    def avatar(self):
        return self.image.url if self.image else static("images/avatar_default.svg")
