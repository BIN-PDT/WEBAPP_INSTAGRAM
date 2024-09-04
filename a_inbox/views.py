from cryptography.fernet import Fernet
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from .forms import *


f = Fernet(settings.ENCRYPT_KEY)


@login_required
def inbox_view(request, conversation_id=None):
    list_conversations = Conversation.objects.filter(participants=request.user)
    if conversation_id:
        conversation = get_object_or_404(list_conversations, id=conversation_id)
        # SEEN MESSAGE.
        lastest_message = conversation.messages.first()
        if not conversation.is_seen and lastest_message.sender != request.user:
            conversation.is_seen = True
            conversation.save()
    else:
        conversation = None

    context = {"list_conversations": list_conversations, "conversation": conversation}
    return render(request, "a_inbox/index.html", context)


@login_required
def search_users(request):
    keyword = request.GET.get("search_user")
    if request.htmx:
        if len(keyword) > 0:
            users = User.objects.filter(
                Q(username__startswith=keyword)
                | Q(profile__realname__icontains=keyword)
            ).exclude(username=request.user.username)

            return render(request, "a_inbox/user_search_result.html", {"users": users})
        else:
            return HttpResponse("")
    else:
        return Http404()


@login_required
def new_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    form = InboxNewMessageForm()

    if request.method == "POST":
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            # ENCRYPT MESSAGE.
            message_original = form.cleaned_data["body"]
            message_bytes = message_original.encode("utf-8")
            message_encrypted = f.encrypt(message_bytes)
            message_decoded = message_encrypted.decode("utf-8")
            message.body = message_decoded

            for conversation in request.user.conversations.all():
                if recipient in conversation.participants.all():
                    message.conversation = conversation
                    message.save()
                    conversation.lastmessage_created = timezone.now()
                    conversation.is_seen = False
                    conversation.save()
                    return redirect("inbox", conversation.id)

            new_conversation = Conversation.objects.create()
            new_conversation.participants.add(request.user, recipient)
            new_conversation.save()
            message.conversation = new_conversation
            message.save()

            return redirect("inbox", new_conversation.id)

    context = {"recipient": recipient, "form": form}
    return render(request, "a_inbox/form_new_message.html", context)


@login_required
def new_reply(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    form = InboxNewMessageForm()

    if request.method == "POST":
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            # ENCRYPT MESSAGE.
            message_original = form.cleaned_data["body"]
            message_bytes = message_original.encode("utf-8")
            message_encrypted = f.encrypt(message_bytes)
            message_decoded = message_encrypted.decode("utf-8")
            message.body = message_decoded

            message.conversation = conversation
            message.save()
            conversation.lastmessage_created = timezone.now()
            conversation.is_seen = False
            conversation.save()

            return redirect("inbox", conversation_id)

    context = {"conversation": conversation, "form": form}
    return render(request, "a_inbox/form_new_reply.html", context)


@login_required
def notify_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    lastest_message = conversation.messages.first()

    if (
        not conversation.is_seen
        and lastest_message
        and lastest_message.sender != request.user
    ):
        return render(request, "a_inbox/notify_icon.html")
    else:
        return HttpResponse("")


@login_required
def notify_inbox(request):
    user = request.user
    list_conversations = Conversation.objects.filter(participants=user, is_seen=False)

    for conversation in list_conversations:
        lastest_message = conversation.messages.first()
        if lastest_message and lastest_message.sender != user:
            return render(request, "a_inbox/notify_icon.html")

    return HttpResponse("")
