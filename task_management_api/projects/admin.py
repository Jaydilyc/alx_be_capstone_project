from django.contrib import admin

# Register your models here.
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'created_at']
    search_fields = ['name', 'owner__username']
    list_filter = ['created_at']