from django.contrib import admin
from .models import Book, Post, UserProfile, Category, Task, SubTask

admin.site.register(Book)
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(SubTask)

