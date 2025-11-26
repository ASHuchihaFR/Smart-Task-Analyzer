from django.contrib import admin
from django.urls import path
from tasks.views import prioritize_tasks_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/prioritize/', prioritize_tasks_api),
]
