from django.urls import path
from . import views

urlpatterns = [
    path('this-or-that/', views.this_or_that, name='this_or_that'),
    path('this-or-that/answer/', views.answer_this_or_that, name='answer_this_or_that'),
    path('truth-or-dare/', views.truth_or_dare, name='truth_or_dare'),
    path('bucket-list/', views.bucket_list, name='bucket_list'),
    path('bucket-list/add/', views.bucket_list_add, name='bucket_list_add'),
    path('bucket-list/<int:pk>/complete/', views.bucket_list_complete, name='bucket_list_complete'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/submit/', views.submit_quiz, name='submit_quiz'),
]
