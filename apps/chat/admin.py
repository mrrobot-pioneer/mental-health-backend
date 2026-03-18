from django.contrib import admin
from .models import Chat, Message

# Register your models here.
@admin.register(Chat)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title', 'emoji')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['short_content', 'role', 'chat', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['content', 'chat__title']
    readonly_fields = ['created_at']

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'
