from django.urls import path
from . import views

urlpatterns = [
    path('', views.memory_list, name='memory_list'),
    path('new/', views.memory_create, name='memory_create'),
    path('<int:pk>/', views.memory_detail, name='memory_detail'),
    path('<int:pk>/delete/', views.memory_delete, name='memory_delete'),
    path('<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
]
