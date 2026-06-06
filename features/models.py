# features/models.py
# UPDATED: Added SavedDateIdea model so users can save favourite date ideas.
# UNCHANGED: All other models exactly as before.

from django.db import models
from django.conf import settings


class OpenWhenMessage(models.Model):
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='open_when_created')
    for_partner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='open_when_received')
    occasion    = models.CharField(max_length=150)
    content     = models.TextField()
    is_opened   = models.BooleanField(default=False)
    opened_at   = models.DateTimeField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class MoodHistory(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='mood_history')
    mood       = models.CharField(max_length=50)
    message    = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class DateIdea(models.Model):
    CATEGORY_CHOICES = [
        ('virtual',      'Virtual 💻'),
        ('indoor',       'Indoor 🏠'),
        ('outdoor',      'Outdoor 🌿'),
        ('budget',       'Budget 💸'),
        ('longdistance', 'Long Distance 💕'),
        ('rainy',        'Rainy Day 🌧️'),
        ('anniversary',  'Anniversary 💍'),
        # keep old categories for backwards compat
        ('creative',     'Creative 🎨'),
        ('chill',        'Chill 🌙'),
    ]
    title           = models.CharField(max_length=200)
    description     = models.TextField()
    category        = models.CharField(max_length=20, choices=CATEGORY_CHOICES,
                                       default='virtual')
    emoji           = models.CharField(max_length=10, default='💑')
    estimated_cost  = models.CharField(max_length=50, blank=True)
    duration        = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title


# NEW: Lets users save favourite date ideas
class SavedDateIdea(models.Model):
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='saved_date_ideas')
    idea     = models.ForeignKey(DateIdea, on_delete=models.CASCADE,
                                 related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'idea']


class Notification(models.Model):
    TYPE_CHOICES = [
        ('message',  '💬 Message'),
        ('mood',     '😊 Mood'),
        ('memory',   '📸 Memory'),
        ('couple',   '💑 Couple'),
        ('open_when','💌 Open When'),
        ('game',     '🎮 Game'),
    ]
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='notifications')
    title      = models.CharField(max_length=200)
    message    = models.TextField()
    notif_type = models.CharField(max_length=20, default='message', choices=TYPE_CHOICES)
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']