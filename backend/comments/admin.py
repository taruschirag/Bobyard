from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'date', 'likes')
    search_fields = ('author', 'text')
    ordering = ('date',)
