from rest_framework import serializers
from .models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    preview = serializers.ReadOnlyField()

    class Meta:
        model = Chat
        fields = [
            'id', 'title', 'emoji', 'preview', 'is_pinned', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'preview', 'created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'content', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']