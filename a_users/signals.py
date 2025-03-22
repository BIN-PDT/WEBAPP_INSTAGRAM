from allauth.account.models import EmailAddress
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, Profile


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        Profile.objects.create(user=user, email=user.email)
    else:
        profile = get_object_or_404(Profile, user=user)
        profile.email = user.email
        profile.save()


@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
    profile = instance
    if not created:
        user = get_object_or_404(User, id=profile.user.id)
        if user.email != profile.email:
            user.email = profile.email
            user.save()


@receiver(post_save, sender=Profile)
def update_email_address(sender, instance, created, **kwargs):
    profile = instance
    if not created:
        try:
            email_address = EmailAddress.objects.get_primary(profile.user)
            if email_address.email != profile.email:
                email_address.email = profile.email
                email_address.verified = False
                email_address.save()
        except:
            pass
