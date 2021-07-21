from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Chat, Message
from django.views import View
from .forms import MessageForm

class ChatsView(View):

    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(member__in=[request.user.id])
        return render(request, 'messages/chat.html', {'user_profile': request.user, 'chats': chats})

class MessagesView(View):

    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.member.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None
        return render(request, 'messages/messages.html', {
            'form': MessageForm(),
            'user_profile': request.user,
            'chat': chat
        })

    def post(self, request, chat_id):
        form = MessageForm(request.POST or None)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.chat_id = chat_id
            new_message.author = request.user
            new_message.save()
            return redirect(reverse('messages', kwargs={'chat_id': chat_id}))
