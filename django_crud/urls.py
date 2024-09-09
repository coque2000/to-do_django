"""
URL configuration for django_crud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('registration/', views.registration, name="registration"),
    path('signup/', views.sign_up, name="signup"),
    path('signin/', views.sign_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks/completed', views.tasks_completed, name="completed-tasks"),
    path('task/create/', views.create_task, name='create-task'),
    path('task/<int:task_id>/', views.task_detail, name='detail-task'),
    path('task/complete/<int:task_id>/', views.task_complete, name='complete-task'),
    path('task/delete/<int:task_id>/', views.task_delete, name='delete-task')
]
