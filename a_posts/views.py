from django.shortcuts import render, redirect
from .models import *
from .forms import *


def home_view(request):
    posts = Post.objects.all()
    return render(request, "a_posts/home.html", {"posts": posts})


def post_create_view(request):
    form = PostCreateForm()

    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    return render(request, "a_posts/post_create.html", {"form": form})
