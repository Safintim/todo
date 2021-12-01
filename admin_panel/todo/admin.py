from django.contrib import admin

from todo.models import Task, TaskList


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title__icontains', 'description__icontains')
    autocomplete_fields = ('list',)


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title__icontains',)
