from django import forms
from .models import Profile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile()
        exclude = ["user"]
        labels = {"realname": "Name"}
        widgets = {
            "image": forms.FileInput(),
            "bio": forms.Textarea({"rows": 3}),
        }
