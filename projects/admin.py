from django.contrib import admin
from .models import Project, Task, MVPRequirement


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'progress', 'owner', 'created_date', 'due_date']
    list_filter = ['status', 'owner', 'created_date']
    search_fields = ['name', 'description']
    date_hierarchy = 'created_date'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'priority', 'completed', 'created_date', 'completed_date']
    list_filter = ['priority', 'completed', 'project', 'created_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_date'


@admin.register(MVPRequirement)
class MVPRequirementAdmin(admin.ModelAdmin):
    list_display = ['description', 'project', 'completed', 'created_date', 'completed_date']
    list_filter = ['completed', 'project', 'created_date']
    search_fields = ['description']
    date_hierarchy = 'created_date'
