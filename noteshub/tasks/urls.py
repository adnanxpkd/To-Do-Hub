from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasks_list, name='tasks_list'),
    path('add/', views.add_task, name='add_task'),
    path('edit/<uuid:pk>/', views.edit_task, name='edit_task'),
    path('delete/<uuid:pk>/', views.delete_task, name='delete_task'),
    path('toggle/<uuid:pk>/', views.toggle_task, name='toggle_task'),
]
