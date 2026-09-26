from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class name")
    
    def __str__(self):
        return self.name

class Test(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    time_limit = models.IntegerField(default=30)  # in minutes
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.topic} - {self.get_difficulty_display()}"

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    options = models.JSONField(default=dict)
    correct_answer = models.CharField(max_length=1)
    explanation = models.TextField(blank=True, help_text="Explanation of the correct answer")

    def __str__(self):
        return f"Question from {self.test}"

class UserResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1)
    is_correct = models.BooleanField(default=False)
    date_answered = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s response to {self.question}"
