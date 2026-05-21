from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'partner', 'current_mood', 'is_coupled']
    fieldsets = UserAdmin.fieldsets + (
        ('Together Profile', {'fields': ('avatar', 'nickname', 'bio', 'partner', 'couple_since', 'anniversary', 'next_meeting', 'current_mood', 'mood_message', 'streak_count', 'theme_preference', 'invite_code')}),
    )
    readonly_fields = ['invite_code']
