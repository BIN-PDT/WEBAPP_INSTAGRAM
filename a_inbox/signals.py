from django.core.mail import EmailMessage
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
                    email_body = "You received a message at Awesome!"

                    email = EmailMessage(email_subject, email_body, to=[email_address])
                    email.send()
                except:
                    pass
