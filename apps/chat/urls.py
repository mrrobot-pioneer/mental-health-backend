from django.urls import path
from .views import create_message, chat_list, chat_messages, rename_chat, pin_chat, delete_chat

urlpatterns = [
    path('', chat_list, name='chat-list'),
    path('create/', create_message, name='create-message'),
    path('<uuid:pk>/messages/', chat_messages, name='chat-messages'),
    path('<uuid:pk>/rename/', rename_chat, name='rename-chat'),
    path('<uuid:pk>/pin/', pin_chat, name='pin-chat'),
    path('<uuid:pk>/delete/', delete_chat, name='delete-chat'),
]