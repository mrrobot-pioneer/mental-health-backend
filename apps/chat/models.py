import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chats',
    )

    # Chat Title
    title = models.CharField(
        max_length=100, 
        blank=True, 
        default=""
    )

    emoji = models.CharField(max_length=10, blank=True, default="💬")

    # pinned
    is_pinned = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title or f"Chat {self.id}"

    @property
    def preview(self):
        """Get content of the last message."""
        last_message = self.messages.order_by('-created_at').first()
        return last_message.content if last_message else ""


class Message(models.Model):

    class Role(models.TextChoices):
        USER = 'user', 'User'
        ASSISTANT = 'assistant', 'Assistant'

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    role = models.CharField(
        max_length=10, 
        choices=Role.choices
    )

    content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role.title()}: {self.content[:100] + '...' if len(self.content) > 100 else self.content}"


    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            Chat.objects.filter(pk=self.chat_id).update(
                updated_at=timezone.now())