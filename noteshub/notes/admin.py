from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'tags', 'is_deleted', 'created_at')
    list_filter = ('is_deleted', 'is_pinned')
    search_fields = ('title', 'tags', 'content')
