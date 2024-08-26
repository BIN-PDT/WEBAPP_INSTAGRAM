import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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
            post = form.save(commit=False)

            website = requests.get(form.data["url"])
            source = BeautifulSoup(website.text, "html.parser")
            # GET IMAGE URL.
            image_result = source.select(
                'meta[content^="https://live.staticflickr.com/"]'
            )
            image = image_result[0]["content"]
            post.image = image
            # GET IMAGE TITLE.
            title_result = source.select("h1.photo-title")
            title = title_result[0].text.strip()
            post.title = title
            # GET IMAGE ARTIST.
            artist_result = source.select("a.owner-name")
            artist = artist_result[0].text.strip()
            post.artist = artist

            post.save()
            return redirect("home")

    return render(request, "a_posts/post_create.html", {"form": form})


def post_delete_view(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted")
        return redirect("home")

    return render(request, "a_posts/post_delete.html", {"post": post})


def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = PostEditForm(instance=post)

    if request.method == "POST":
        form = PostEditForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated")
            return redirect("home")

    context = {"post": post, "form": form}
    return render(request, "a_posts/post_edit.html", context)


def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)

    return render(request, "a_posts/post_page.html", {"post": post})
