from django.contrib import admin
from .models import Task
from django.contrib.auth.models import User


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'status', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status',)