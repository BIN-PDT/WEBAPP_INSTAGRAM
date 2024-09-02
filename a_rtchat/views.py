from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


@login_required
def chat_view(request, chatroom_name="public-chat"):
    user = request.user
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatMessageCreateForm()

    partner = None
    if chat_group.is_private:
        if user not in chat_group.members.all():
            raise Http404()
        else:
            for member in chat_group.members.all():
                if member != user:
                    partner = member
                    break

    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.author = request.user
            chat_message.group = chat_group
            chat_message.save()

            context = {"message": chat_message}
            return render(request, "a_rtchat/partials/chat_message.html", context)

    context = {
        "chat_messages": chat_messages,
        "form": form,
        "partner": partner,
        "chatroom_name": chatroom_name,
    }
    return render(request, "a_rtchat/index.html", context)


@login_required
def get_or_create_chatroom(request, username):
    user = request.user
    if user.username == username:
        return redirect("chat")

    partner = get_object_or_404(User, username=username)
    private_chatrooms = user.chat_groups.filter(is_private=True)

    for chatroom in private_chatrooms:
        if partner in chatroom.members.all():
            return redirect("chatroom", chatroom.group_name)

    chatroom = ChatGroup.objects.create(is_private=True)
    chatroom.members.add(user, partner)
    return redirect("chatroom", chatroom.group_name)
