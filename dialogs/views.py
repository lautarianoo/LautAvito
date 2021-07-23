from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Chat, Message
from django.views import View
from .forms import MessageForm
from advertisements.models import Advertise

class ChatsView(View):

    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(member__in=[request.user.id])
        return render(request, 'messages/chat.html', {'user_profile': request.user, 'chats': chats})

class MessagesView(View):

    def get(self, request, *args, **kwargs):
        try:
            chat = Chat.objects.get(id=kwargs.get('pk'))
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

    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST or None)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.chat_id = kwargs.get('pk')
            new_message.author = request.user
            new_message.save()
            return redirect(reverse('messages', kwargs={'pk': kwargs.get('pk')}))

class CreateDialogView(View):

    def get(self, request, *args, **kwargs):
        advertise = Advertise.objects.get(id=kwargs.get('pk'))
        componion = advertise.seller
        chats = Chat.objects.filter(member__in=[request.user.id, componion.id], advertise=advertise)
        if chats.count() == 0:
            chat = Chat.objects.create(start_user=request.user, advertise=advertise)
            chat.member.add(request.user)
            chat.member.add(componion)
            chat.save()
        else:
            chat = chats.first()
        return redirect(reverse('messages', kwargs={'pk': chat.id}))
