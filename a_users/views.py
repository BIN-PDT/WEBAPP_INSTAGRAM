from django.http import Http404
from django.urls import reverse
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from a_posts.forms import ReplyCreateForm


def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
    posts = profile.user.posts.all()

    if request.htmx:
        if "top-posts" in request.GET:
            posts = (
                profile.user.posts.annotate(likes_count=Count("likes"))
                .filter(likes__isnull=False)
                .order_by("-likes_count")
            )

            template = "snippets/profile_filter_posts.html"
            context = {"posts": posts}
        elif "top-comments" in request.GET:
            comments = (
                profile.user.comments.annotate(likes_count=Count("likes"))
                .filter(likes__isnull=False)
                .order_by("-likes_count")
            )

            template = "snippets/profile_filter_comments.html"
            context = {"comments": comments, "reply_form": ReplyCreateForm()}
        elif "liked-posts" in request.GET:
            posts = profile.user.liked_posts.order_by("-likedpost__created")

            template = "snippets/profile_filter_posts.html"
            context = {"posts": posts}
        else:
            template = "snippets/profile_filter_posts.html"
            context = {"posts": posts}

        return render(request, template, context)

    context = {"profile": profile, "posts": posts}
    return render(request, "a_users/profile.html", context)


@login_required
def profile_edit_view(request):
    profile = request.user.profile
    form = ProfileEditForm(instance=profile)

    if request.method == "POST":
        form = ProfileEditForm(instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("profile")

    if request.path == reverse("profile-onboarding"):
        template = "a_users/profile_onboarding.html"
    else:
        template = "a_users/profile_edit.html"

    return render(request, template, {"form": form})


@login_required
def profile_delete_view(request):
    user = request.user

    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, "Account deleted, what a pity!")
        return redirect("home")

    return render(request, "a_users/profile_delete.html")
