from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *


@login_required
def inbox_view(request, conversation_id=None):
    list_conversations = Conversation.objects.filter(participants=request.user)
    if conversation_id:
        conversation = get_object_or_404(list_conversations, id=conversation_id)
    else:
        conversation = None

    context = {"list_conversations": list_conversations, "conversation": conversation}
    return render(request, "a_inbox/index.html", context)
