from django.urls import path
from . import views

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('upload/', views.album_upload, name='album_upload'),
    path('album/<uuid:pk>/', views.album_detail, name='album_detail'),
    path('album/<uuid:pk>/edit/', views.album_edit, name='album_edit'),
    path('album/<uuid:pk>/delete/', views.album_delete, name='album_delete'),
]
