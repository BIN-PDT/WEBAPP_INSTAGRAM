from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["url", "body"]
        labels = {"url": "", "body": ""}
        widgets = {
            "url": forms.URLInput(
                {
                    "placeholder": "Add an URL",
                    "class": "italic",
                }
            ),
            "body": forms.Textarea(
                {
                    "rows": 3,
                    "placeholder": "Add a caption...",
                    "class": "font-1 text-4xl",
                }
            ),
        }
