from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        labels = {
            "body": "",
        }
        widgets = {
            "body": forms.Textarea(
                {
                    "rows": 3,
                    "placeholder": "Add a caption...",
                    "class": "font-1 text-4xl",
                }
            ),
        }
