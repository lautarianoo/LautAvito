from django.urls import path
from .views import *

urlpatterns = [
    path('', ChatsView.as_view(), name='chats'),
    path('<int:pk>/', MessagesView.as_view(), name='messages')
]
