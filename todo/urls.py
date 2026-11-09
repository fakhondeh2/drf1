"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path
from . import views

app_name = 'todo_urls'
urlpatterns = [
    path('', views.all_todos, name='todo_list'),
    path('cbv', views.TodoList.as_view(), name='todo_list_class_base_view'),

    path('cbv/<pk>', views.Todo_detail_api_view.as_view(), name='detail_todo_class_base_view'),
    path('<todo_id>', views.todo_detail_view, name='detail_list'),


]

