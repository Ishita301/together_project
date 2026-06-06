# games/urls.py
# UPDATED: All routes match the corrected views.py

from django.urls import path
from . import views

urlpatterns = [
    # Truth or Dare
    path('truth-dare/',                     views.truth_dare,     name='truth_dare'),

    # This or That
    path('this-or-that/',                   views.this_or_that,   name='this_or_that'),
    path('this-or-that/answer/',            views.answer_tot,     name='answer_tot'),

    # Quiz
    path('quiz/',                           views.quiz,           name='quiz'),
    path('quiz/submit/',                    views.submit_quiz,    name='submit_quiz'),

    # Date Ideas
    path('date-ideas/',                     views.date_ideas,     name='date_ideas'),
    path('date-ideas/<int:pk>/save/',       views.save_date_idea, name='save_date_idea'),

    # Bucket List
    path('bucket-list/',                    views.bucket_list,    name='bucket_list'),
    path('bucket-list/<int:pk>/toggle/',    views.toggle_bucket,  name='toggle_bucket'),
]