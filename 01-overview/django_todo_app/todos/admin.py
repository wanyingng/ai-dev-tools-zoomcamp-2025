from django.contrib import admin
from .models import TodoItem


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    """Admin interface for TodoItem model."""
    
    list_display = ('title', 'due_date', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'due_date', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_resolved',)
    date_hierarchy = 'created_at'
    ordering = ('due_date', '-created_at')

