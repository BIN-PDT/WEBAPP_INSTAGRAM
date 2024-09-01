from django import forms
from .models import Profile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
        labels = {"image": "", "realname": "", "email": "", "location": "", "bio": ""}
        widgets = {
            "image": forms.FileInput(
                {
                    "accept": "image/*",
                    "class": "!px-5 py-0",
                }
            ),
            "realname": forms.TextInput(
                {
                    "placeholder": "Add name",
                }
            ),
            "email": forms.EmailInput(
                {
                    "readonly": "readonly",
                    "placeholder": "Add email",
                    "class": "text-gray-500 focus:outline-none",
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


class ProfileEmailEdit(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["email"]
        labels = {"email": ""}
        widgets = {"email": forms.EmailInput()}
