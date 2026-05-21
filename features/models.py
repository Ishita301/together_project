from django.db import models
from django.conf import settings

class OpenWhenMessage(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='open_when_created')
    for_partner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='open_when_received')
    occasion = models.CharField(max_length=100)
    content = models.TextField()
    is_opened = models.BooleanField(default=False)
    opened_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    OCCASION_CHOICES = [
        ('sad','You are feeling sad'),('angry','You are angry at me'),
        ('missing','You are missing me'),('happy','You are feeling happy'),
        ('stressed','You are stressed'),('birthday','It is your birthday'),
        ('lonely','You feel lonely'),('custom','Custom'),
    ]

class MoodHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mood = models.CharField(max_length=50)
    message = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    MOOD_CHOICES = [
        ('happy','😊 Happy'),('missing','💭 Missing You'),('busy','💼 Busy'),
        ('tired','😴 Tired'),('sad','😢 Sad'),('excited','🎉 Excited'),
        ('love','❤️ Feeling Loved'),('anxious','😰 Anxious'),
    ]

class DateIdea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('virtual','Virtual'),('physical','Physical'),('creative','Creative'),('chill','Chill')
    ])
    emoji = models.CharField(max_length=10, default='💑')

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notif_type = models.CharField(max_length=30, default='general')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
