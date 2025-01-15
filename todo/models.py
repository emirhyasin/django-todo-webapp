from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Todo(models.Model):
    PRIORITY_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]
    
    date_day = models.CharField(max_length=2, default="01")
    date_month = models.CharField(max_length=3, default="01")
    user = models.ForeignKey(
        User, related_name="tasks",
        on_delete=models.DO_NOTHING    
        )
    title = models.CharField(max_length=50)
    body = models.TextField()
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    
    def __str__(self):
        return self.title
