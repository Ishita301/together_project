from django.db import models
from django.conf import settings

class ThisOrThatQuestion(models.Model):
    question = models.CharField(max_length=200)
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    emoji_a = models.CharField(max_length=10, default='☕')
    emoji_b = models.CharField(max_length=10, default='🍵')

class ThisOrThatAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(ThisOrThatQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, choices=[('A','A'),('B','B')])
    created_at = models.DateTimeField(auto_now_add=True)

class QuizQuestion(models.Model):
    question = models.CharField(max_length=300)
    correct_answer = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    category = models.CharField(max_length=50, default='general')

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class TruthOrDare(models.Model):
    content = models.TextField()
    type = models.CharField(max_length=10, choices=[('truth','Truth'),('dare','Dare')])
    category = models.CharField(max_length=20, choices=[
        ('cute','Cute'),('funny','Funny'),('romantic','Romantic'),('deep','Deep')
    ], default='cute')

class BucketListItem(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=[
        ('travel','Travel'),('experience','Experience'),('goal','Goal'),('dream','Dream')
    ], default='dream')
    is_completed = models.BooleanField(default=False)
    target_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
