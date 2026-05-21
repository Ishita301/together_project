from django.db import models
from django.conf import settings

class Memory(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memories')
    title = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='memories/', null=True, blank=True)
    video_url = models.URLField(blank=True)
    memory_date = models.DateField()
    tags = models.CharField(max_length=200, blank=True)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    CATEGORY_CHOICES = [
        ('first','First Times'),('travel','Travel'),('celebration','Celebrations'),
        ('everyday','Everyday'),('milestone','Milestones'),('other','Other')
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')

    class Meta:
        ordering = ['-memory_date']

    def __str__(self):
        return self.title
