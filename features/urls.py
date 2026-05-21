from django.urls import path
from . import views

urlpatterns = [
    path('open-when/', views.open_when_list, name='open_when_list'),
    path('open-when/create/', views.open_when_create, name='open_when_create'),
    path('open-when/<int:pk>/read/', views.open_when_read, name='open_when_read'),
    path('date-ideas/', views.date_ideas, name='date_ideas'),
    path('notifications/', views.notifications, name='notifications'),
    path('mood-history/', views.mood_history, name='mood_history'),
]
