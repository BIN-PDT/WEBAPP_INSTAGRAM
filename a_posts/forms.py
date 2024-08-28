from django import forms
from .models import Post, Comment, Reply


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["url", "body", "tags"]
        labels = {"url": "", "body": "", "tags": "Category"}
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
                    "class": "font-1 text-4xl mb-0",
                }
            ),
            "tags": forms.CheckboxSelectMultiple(),
        }


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["body", "tags"]
        labels = {"body": "", "tags": "Category"}
        widgets = {
            "body": forms.Textarea(
                {
                    "rows": 3,
                    "placeholder": "Add a caption...",
                    "class": "font-1 text-4xl",
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
                    "class": "placeholder:italic",
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
                    "class": "text-sm placeholder:italic",
                }
            ),
        }
