from django.shortcuts import render
from .models import Chat, Message
from django.views import View

class ChatsView(View):

    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(member__in=[request.user.id])
        return render(request, 'messages/chat.html', {'user_profile': request.user, 'chats': chats})
