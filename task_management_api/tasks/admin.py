from django.contrib import admin

# Register your models here.
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'project', 'priority', 'status', 'due_date', 'completed_at']
    search_fields = ['title', 'owner__username', 'project__name']
    list_filter = ['priority', 'status', 'created_at', 'due_date']