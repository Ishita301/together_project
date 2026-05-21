from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('connect/', views.connect_partner, name='connect_partner'),
    path('disconnect/', views.disconnect_partner, name='disconnect_partner'),
    path('update-mood/', views.update_mood, name='update_mood'),
]
