from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_list, name='notes_list'),
    path('add/', views.add_note, name='add_note'),
    path('edit/<uuid:pk>/', views.edit_note, name='edit_note'),
    path('delete/<uuid:pk>/', views.delete_note, name='delete_note'),
    path('trash/', views.trash_list, name='trash_list'),
    path('restore/<uuid:pk>/', views.restore_note, name='restore_note'),
    path('delete_forever/<uuid:pk>/', views.delete_permanently, name='delete_forever'),
]
