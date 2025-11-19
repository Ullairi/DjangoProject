from django.contrib import admin
from .models import Book, Post, UserProfile, Category, Task, SubTask

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ('title', 'description', 'status', 'deadline')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title_short', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title',)
    date_hierarchy = 'created_at'
    inlines = [SubTaskInline]

    def title_short(self, task):
        if len(task.title) > 10:
            return f"{task.title[:10]}..."
        return task.title
    title_short.short_description = "Short title"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title',)
    date_hierarchy = 'created_at'
    actions = ['object_done']

    def object_done(self, request, queryset):
        updated = queryset.update(status='done')
        self.message_user(request, f"{updated} subtask is in 'Done' status now")
    object_done.short_description = "Chosen subtasks now marked as 'Done'"


admin.site.register(Book)
admin.site.register(Post)
admin.site.register(UserProfile)

