from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import *
from .forms import *


@login_required
def chat_view(request, group_name="public-chat"):
    user = request.user
    chatroom = get_object_or_404(ChatGroup, group_name=group_name)
    chat_messages = chatroom.chat_messages.all()[:30]
    form = GroupMessageCreateForm()
    # PRIVATE MODE.
    partner = None
    if chatroom.is_private:
        if not chatroom.members.contains(user):
            raise Http404()
        else:
            partner = chatroom.members.exclude(id=user.id).first()

    # GROUP MODE.
    if chatroom.groupchat_name:
        if not chatroom.members.contains(user):
            chatroom.members.add(user)

    context = {
        "group_name": group_name,
        "chat_messages": chat_messages,
        "form": form,
        "partner": partner,
        "chatroom": chatroom,
    }
    return render(request, "a_rtchat/index.html", context)


@login_required
def create_private_chatroom(request, username):
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


@login_required
def groupchat_create_view(request):
    form = ChatGroupCreateForm()

    if request.method == "POST":
        form = ChatGroupCreateForm(request.POST)
        if form.is_valid():
            chatroom = form.save(commit=False)
            chatroom.admin = request.user
            chatroom.save()
            chatroom.members.add(request.user)
            return redirect("chatroom", chatroom.group_name)

    return render(request, "a_rtchat/groupchat_create.html", {"form": form})


@login_required
def groupchat_edit_view(request, group_name):
    chatroom = get_object_or_404(ChatGroup, group_name=group_name, admin=request.user)
    form = ChatGroupEditForm(instance=chatroom)

    if request.method == "POST":
        form = ChatGroupEditForm(instance=chatroom, data=request.POST)
        if form.is_valid():
            form.save()

            removed_members = request.POST.getlist("removed_members")
            removed_users = User.objects.filter(id__in=removed_members)
            chatroom.members.remove(*removed_users)

            channel_layer = get_channel_layer()
            event = {
                "type": "chatroom_handler",
                "chatroom_name": form.cleaned_data["groupchat_name"],
            }
            async_to_sync(channel_layer.group_send)(group_name, event)

            messages.success(request, "Chatroom updated!")
            return redirect("chatroom", group_name)

    context = {"form": form, "chatroom": chatroom}
    return render(request, "a_rtchat/groupchat_edit.html", context)


@login_required
def groupchat_delete_view(request, group_name):
    chatroom = get_object_or_404(ChatGroup, group_name=group_name, admin=request.user)

    if request.method == "POST":
        chatroom.delete()

        channel_layer = get_channel_layer()
        event = {"type": "chatroom_handler", "chatroom_name": chatroom.groupchat_name}
        async_to_sync(channel_layer.group_send)(group_name, event)

        messages.success(request, "Chatroom deleted!")
        return redirect("home")

    return render(request, "a_rtchat/groupchat_delete.html", {"chatroom": chatroom})


@login_required
def leave_groupchat(request, group_name):
    chatroom = get_object_or_404(ChatGroup, group_name=group_name)
    if not chatroom.members.contains(request.user):
        raise Http404()

    if request.method == "POST":
        chatroom.members.remove(request.user)
        messages.success(request, "You left the Chat!")
        return redirect("home")


@login_required
def chat_file_upload(request, group_name):
    chatroom = get_object_or_404(ChatGroup, group_name=group_name)

    if request.htmx and request.FILES:
        message = GroupMessage.objects.create(
            author=request.user,
            group=chatroom,
            file=request.FILES["file"],
        )

        channel_layer = get_channel_layer()
        event = {"type": "message_handler", "message_id": message.id}
        async_to_sync(channel_layer.group_send)(group_name, event)

    return HttpResponse()


@login_required
def check_member(request, group_name):
    try:
        chatroom = ChatGroup.objects.get(group_name=group_name)
        is_member = chatroom.members.contains(request.user)
    except:
        is_member = False

    return JsonResponse({"is_member": is_member})
