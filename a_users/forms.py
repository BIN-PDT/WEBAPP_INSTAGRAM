from django import forms
from .models import Profile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile()
        exclude = ["user"]
        labels = {"image": "", "realname": "", "email": "", "location": "", "bio": ""}
        widgets = {
            "image": forms.FileInput(),
            "realname": forms.TextInput(
                {
                    "placeholder": "Add name",
                }
            ),
            "email": forms.EmailInput(
                {
                    "placeholder": "Add email",
                }
            ),
            "location": forms.TextInput(
                {
                    "placeholder": "Add location",
                }
            ),
            "bio": forms.Textarea(
                {
                    "rows": 3,
                    "placeholder": "Add biography",
                }
            ),
        }
