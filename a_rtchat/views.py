from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="public-chat")
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatMessageCreateForm()

    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.author = request.user
            chat_message.group = chat_group
            chat_message.save()

            context = {"message": chat_message}
            return render(request, "a_rtchat/partials/chat_message_p.html", context)

    context = {"chat_messages": chat_messages, "form": form}
    return render(request, "a_rtchat/index.html", context)
