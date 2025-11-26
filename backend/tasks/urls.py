from django.urls import path
from .views import analyze_tasks, suggest_tasks, prioritize_tasks_api

urlpatterns = [
    path('analyze/', analyze_tasks),
    path('suggest/', suggest_tasks),
    path('prioritize/', prioritize_tasks_api),
]
