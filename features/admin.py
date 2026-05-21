from django.contrib import admin
from .models import *

admin.site.register(OpenWhenMessage)
admin.site.register(MoodHistory)

@admin.register(DateIdea)
class DateIdeaAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'emoji']

admin.site.register(Notification)
