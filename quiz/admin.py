from django.contrib import admin
from .models import Category, Test, Question, UserResponse

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'topic', 'difficulty', 'score', 'time_limit', 'date_created')
    list_filter = ('category', 'difficulty', 'date_created')
    search_fields = ('topic', 'user__username', 'category__name')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'text', 'correct_answer')
    list_filter = ('test__category', 'test__difficulty')
    search_fields = ('text', 'test__topic')

@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'is_correct', 'date_answered')
    list_filter = ('is_correct', 'date_answered', 'question__test__category')
    search_fields = ('user__username', 'question__text')
