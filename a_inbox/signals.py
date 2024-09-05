from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import InboxMessage


@receiver(post_save, sender=InboxMessage)
def send_inbox_notification(sender, instance, created, **kwargs):
    message = instance
    if created:
        for participant in message.conversation.participants.all():
            if participant != message.sender:
                try:
                    email_address = participant.emailaddress_set.get(
                        primary=True, verified=True
                    )
                    email_subject = f"New Message from {message.sender.profile.name}"
                    html_message = render_to_string(
                        "a_inbox/email/inbox_notification.html"
                    )
                    email_body = strip_tags(html_message)

                    email = EmailMultiAlternatives(
                        email_subject, email_body, to=[email_address]
                    )
                    email.attach_alternative(html_message, "text/html")
                    email.send()
                except:
                    pass
