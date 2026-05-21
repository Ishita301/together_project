from django.contrib import admin
from .models import *

@admin.register(ThisOrThatQuestion)
class TotAdmin(admin.ModelAdmin):
    list_display = ['question', 'option_a', 'option_b']

@admin.register(TruthOrDare)
class TodAdmin(admin.ModelAdmin):
    list_display = ['type', 'category', 'content']
    list_filter = ['type', 'category']

@admin.register(QuizQuestion)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['question', 'correct_answer', 'category']

admin.site.register(BucketListItem)
admin.site.register(ThisOrThatAnswer)
admin.site.register(QuizAttempt)
