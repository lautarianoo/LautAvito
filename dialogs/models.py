from django.contrib.auth import get_user_model
from django.db import models
from advertisements.models import Advertise

User = get_user_model()

class Chat(models.Model):

    advertise = models.ForeignKey(Advertise, verbose_name='Объявление', on_delete=models.CASCADE)
    member = models.ManyToManyField(User, verbose_name='Участники чата', related_name='chat')
    start_user = models.ForeignKey(User, verbose_name='Пользователь, начавший диалог', related_name='chats', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"

class Message(models.Model):

    chat = models.ForeignKey(Chat, verbose_name='Чат', on_delete=models.CASCADE)
    message = models.TextField(verbose_name='Сообщение')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    author = models.ForeignKey(User, verbose_name='Автор сообщениы', on_delete=models.CASCADE)
    is_readed = models.BooleanField(default=False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return f"Чат - {self.chat.id} | Автор - {self.author}"
