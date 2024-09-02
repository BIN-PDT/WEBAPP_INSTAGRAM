from django import forms
from .models import GroupMessage


class ChatMessageCreateForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ["body"]
        labels = {"body": ""}
        widgets = {
            "body": forms.TextInput(
                attrs={
                    "placeholder": "Type your message here",
                    "class": "p-4 font-4 text-black",
                    "maxlength": "300",
                    "autofocus": True,
                }
            ),
        }
