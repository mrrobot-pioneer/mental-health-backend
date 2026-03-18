from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Q

import logging
import datetime

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

logger = logging.getLogger(__name__)

CONTENT_LENGTH = 500

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_message(request):
    """
    Send a message and get AI response.

    Request: { "chat_id": "uuid" or null, "content": "..." }
    Response: { "chat_id": "...", "content": "..." }
    """

    user = request.user
    content = request.data.get('content', '').strip()
    chat_id = request.data.get('chat_id')

    # can i move the validation to serializer?

    if not content:
        return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

    if len(content) > CONTENT_LENGTH:
        return Response({
            'error': f'Content is too long (Max: {CONTENT_LENGTH} chars)'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get or create chat
    if chat_id:
        chat = get_object_or_404(Chat, id=chat_id)
    else:
        chat = Chat.objects.create(
            user=user,
            title=f"New Chat Created On {datetime.now()}"
        )

    # simulate assistant message
    assistant_reply = "Hello there. How can I help you today?"

    # Save user message only after successful assistant reply
    with transaction.atomic():

        Message.objects.create(
            chat=chat,
            content=content,
            role=Message.Role.USER
        )

        Message.objects.create(
            chat=chat,
            content=assistant_reply,
            role=Message.Role.ASSISTANT
        )

    return Response({
        'chat_id': str(chat.id),
        'content': assistant_reply
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_list(request):
    q = request.GET.get("q")
    filter_type = request.GET.get("filter")

    chats = Chat.objects.filter(user=request.user)

    if q:
        chats = chats.filter(
            Q(title__icontains=q) |
            Q(messages__content__icontains=q)
        ).distinct()

    if filter_type == "pinned":
        chats = chats.filter(is_pinned=True)

    if filter_type == "this-week":
        from django.utils import timezone
        from datetime import timedelta

        chats = chats.filter(
            updated_at__gte=timezone.now() - timedelta(days=7)
        )

    chats = chats.order_by("-is_pinned", "-updated_at")

    serializer = ChatSerializer(chats, many=True)

    return Response(serializer.data)


def chat_messages(request, pk):
    pass


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def rename_chat(request, pk):
    try:
        chat = Chat.objects.get(pk=pk, user=request.user)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)

    title = request.data.get("title")

    if not title:
        return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    title = title.strip()
    
    if len(title) > 100:
        return Response(
            {"error": "Title must be 100 characters or less"},
            status=status.HTTP_400_BAD_REQUEST
        )

    chat.title = title
    chat.save()

    return Response({
        "message": "Chat renamed successfully",
        "data": {
            "id": str(chat.id),
            "title": chat.title
        }
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def pin_chat(request, pk):
    try:
        chat = Chat.objects.get(pk=pk, user=request.user)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)

    is_pinned = request.data.get("is_pinned")

    if is_pinned is None:
        return Response({"error": "Pinned value is required"}, status=status.HTTP_400_BAD_REQUEST)

    chat.is_pinned = bool(is_pinned)
    chat.save()

    return Response({
        "message": "Chat updated successfully",
        "data": {
            "id": str(chat.id),
            "is_pinned": chat.is_pinned
        }
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_chat(request, pk):
    try:
        chat = Chat.objects.get(pk=pk, user=request.user)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)

    chat.delete()

    return Response({
        "message": "Chat deleted successfully"
    }, status=status.HTTP_204_NO_CONTENT)