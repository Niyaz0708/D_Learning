from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('quick-revision/', views.quick_revision, name='quick_revision'),
    path('generate-test/', views.generate_test, name='generate_test'),
    path('take-test/<int:test_id>/', views.take_test, name='take_test'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
] 