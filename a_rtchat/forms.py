from django import forms
from .models import GroupMessage, ChatGroup


class GroupMessageCreateForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ["body"]
        labels = {"body": ""}
        widgets = {
            "body": forms.TextInput(
                {
                    "placeholder": "Type your message here",
                    "class": "p-4 font-4 text-black",
                    "maxlength": "300",
                    "autofocus": True,
                }
            ),
        }


class ChatGroupCreateForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ["groupchat_name"]
        labels = {"groupchat_name": ""}
        widgets = {
            "groupchat_name": forms.TextInput(
                {
                    "placeholder": "Group name",
                    "class": "mb-4 p-4 font-4",
                    "maxlength": "300",
                    "autofocus": True,
                }
            ),
        }


class ChatGroupEditForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ["groupchat_name"]
        labels = {"groupchat_name": ""}
        widgets = {
            "groupchat_name": forms.TextInput(
                {
                    "placeholder": "Group name",
                    "class": "mb-4 p-4 font-4",
                    "maxlength": "300",
                    "autofocus": True,
                }
            ),
        }
