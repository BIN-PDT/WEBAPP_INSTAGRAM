import requests
from bs4 import BeautifulSoup
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
