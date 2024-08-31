from django import forms
from .models import InboxMessage


class InboxNewMessageForm(forms.ModelForm):
    class Meta:
        model = InboxMessage
        fields = ["body"]
        labels = {"body": ""}
        widgets = {
            "body": forms.Textarea(
                {
                    "rows": 4,
                    "placeholder": "Type your message here",
                    "class": "placeholder:italic",
                }
            )
        }
