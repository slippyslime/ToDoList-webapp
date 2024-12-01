from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('task/<int:task_id>/subtask/add/', views.add_subtask, name='add_subtask'),
    path('subtask/<int:subtask_id>/toggle/', views.toggle_subtask, name='toggle_subtask'),
    path('init_data/', views.init_data, name='init_data'),
]