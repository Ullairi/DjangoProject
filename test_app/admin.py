from django.contrib import admin
from .models import Book, Post, UserProfile, Category, Task, SubTask

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title',)
    date_hierarchy = 'created_at'

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title',)
    date_hierarchy = 'created_at'

admin.site.register(Book)
admin.site.register(Post)
admin.site.register(UserProfile)

