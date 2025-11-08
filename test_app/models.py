from django.contrib.auth.models import User
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    def __str__(self):
        return f"Book '{self.title}' -- Author '{self.author}'"

class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(null=True, blank=True)

class UserProfile(models.Model):
    nickname = models.CharField(max_length=120, unique=True)
    bio = models.TextField(null=True, blank=True)
    website = models.URLField(max_length=250, null=True, blank=True)
    age = models.PositiveIntegerField()
    followers_count = models.PositiveIntegerField()
    posts_count = models.PositiveIntegerField()
    comments_count = models.PositiveIntegerField()
    engagement_rate = models.FloatField()

STATUS_CHOICES = [
    ('new', 'New'),
    ('in progress', 'In progress'),
    ('pending', 'Pending'),
    ('blocked', 'Blocked'),
    ('done', 'Done')
]
class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    categories = models.ManyToManyField(Category, blank=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='new')
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SubTask(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} is subtask of {self.task.title}"
