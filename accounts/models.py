from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    nickname = models.CharField(max_length=50, blank=True)
    invite_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    partner = models.OneToOneField('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='partner_of')
    couple_since = models.DateField(null=True, blank=True)
    anniversary = models.DateField(null=True, blank=True)
    next_meeting = models.DateField(null=True, blank=True)
    current_mood = models.CharField(max_length=50, blank=True, default='happy')
    mood_message = models.CharField(max_length=200, blank=True)
    streak_count = models.IntegerField(default=0)
    last_active = models.DateTimeField(auto_now=True)
    theme_preference = models.CharField(max_length=20, default='light', choices=[('light','Light'),('dark','Dark')])

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return f"https://api.dicebear.com/7.x/adventurer/svg?seed={self.username}"

    def is_coupled(self):
        return self.partner is not None

    def __str__(self):
        return self.username
