from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('send-image/', views.send_image, name='send_image'),
]
