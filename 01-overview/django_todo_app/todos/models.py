from django.db import models


class TodoItem(models.Model):
    """Model representing a TODO item."""
    
    title = models.CharField(max_length=200, help_text="Title of the TODO item")
    description = models.TextField(blank=True, help_text="Optional detailed description")
    due_date = models.DateTimeField(null=True, blank=True, help_text="Optional due date")
    is_resolved = models.BooleanField(default=False, help_text="Whether the TODO is completed")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the TODO was created")
    
    class Meta:
        ordering = ['due_date', '-created_at']  # Order by due date first, then by newest
    
    def __str__(self):
        return self.title
