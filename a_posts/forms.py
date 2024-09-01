from django import forms
from .models import Post, Comment, Reply


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["url", "body", "tags"]
        labels = {"url": "", "body": "", "tags": ""}
        widgets = {
            "url": forms.URLInput(
                {
                    "pattern": r"^https?://.*\.(png|jpg|jpeg|gif|svg)$",
                    "placeholder": "Add an URL",
                    "class": "font-4 placeholder:italic",
                }
            ),
            "body": forms.Textarea(
                {
                    "rows": 3,
                    "placeholder": "Add a caption...",
                    "class": "mb-0 font-1 text-4xl",
                }
            ),
            "tags": forms.CheckboxSelectMultiple(),
        }


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["body", "tags"]
        labels = {"body": "", "tags": ""}
        widgets = {
            "body": forms.Textarea(
                {
                    "rows": 3,
                    "placeholder": "Add a caption...",
                    "class": "mb-0 font-1 text-4xl",
                }
            ),
            "tags": forms.CheckboxSelectMultiple(),
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {"body": ""}
        widgets = {
            "body": forms.TextInput(
                {
                    "placeholder": "Leave your comment here",
                    "class": "font-4 placeholder:italic",
                }
            ),
        }


class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["body"]
        labels = {"body": ""}
        widgets = {
            "body": forms.TextInput(
                {
                    "placeholder": "Leave your reply here",
                    "class": "font-4 placeholder:italic",
                }
            ),
        }
