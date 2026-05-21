from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import *
import random

@login_required
def this_or_that(request):
    user = request.user
    questions = list(ThisOrThatQuestion.objects.all())
    answered_ids = list(ThisOrThatAnswer.objects.filter(user=user).values_list('question_id', flat=True))
    unanswered = [q for q in questions if q.id not in answered_ids]
    question = random.choice(unanswered) if unanswered else (random.choice(questions) if questions else None)
    partner_answer = None
    match_count = 0
    total_compared = 0
    if user.partner and question:
        partner_answer = ThisOrThatAnswer.objects.filter(user=user.partner, question=question).first()
        my_answers = ThisOrThatAnswer.objects.filter(user=user)
        for ans in my_answers:
            partner_ans = ThisOrThatAnswer.objects.filter(user=user.partner, question=ans.question).first()
            if partner_ans:
                total_compared += 1
                if ans.answer == partner_ans.answer:
                    match_count += 1
    match_pct = int((match_count / total_compared * 100)) if total_compared else 0
    return render(request, 'games/this_or_that.html', {
        'question': question, 'partner_answer': partner_answer,
        'match_pct': match_pct, 'total_compared': total_compared,
    })

@login_required
def answer_this_or_that(request):
    if request.method == 'POST':
        q_id = request.POST.get('question_id')
        answer = request.POST.get('answer')
        question = get_object_or_404(ThisOrThatQuestion, id=q_id)
        ThisOrThatAnswer.objects.update_or_create(
            user=request.user, question=question,
            defaults={'answer': answer}
        )
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Bad request'}, status=400)

@login_required
def truth_or_dare(request):
    category = request.GET.get('category', 'cute')
    tod_type = request.GET.get('type', 'truth')
    items = list(TruthOrDare.objects.filter(category=category, type=tod_type))
    item = random.choice(items) if items else None
    categories = [('cute','Cute 🌸'), ('funny','Funny 😂'), ('romantic','Romantic 💕'), ('deep','Deep 💭')]
    return render(request, 'games/truth_or_dare.html', {
        'item': item, 'category': category, 'tod_type': tod_type,
        'categories': categories
    })

@login_required
def bucket_list(request):
    user = request.user
    if not user.is_coupled():
        return redirect('connect_partner')
    items = BucketListItem.objects.filter(created_by__in=[user, user.partner])
    return render(request, 'games/bucket_list.html', {'items': items})

@login_required
def bucket_list_add(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        category = request.POST.get('category', 'dream')
        target_date = request.POST.get('target_date') or None
        if title:
            BucketListItem.objects.create(
                created_by=request.user, title=title,
                description=description, category=category,
                target_date=target_date
            )
            messages.success(request, 'Added to bucket list! 🌟')
    return redirect('bucket_list')

@login_required
def bucket_list_complete(request, pk):
    item = get_object_or_404(BucketListItem, pk=pk)
    from django.utils import timezone
    item.is_completed = not item.is_completed
    item.completed_at = timezone.now() if item.is_completed else None
    item.save()
    return JsonResponse({'is_completed': item.is_completed})

@login_required
def quiz(request):
    questions = list(QuizQuestion.objects.all()[:10])
    if not questions:
        return render(request, 'games/quiz.html', {'no_questions': True})
    import json
    import random as r
    questions_data = []
    for q in questions:
        opts = [q.correct_answer, q.option_b, q.option_c, q.option_d]
        r.shuffle(opts)
        questions_data.append({
            'id': q.id, 'question': q.question,
            'options': opts, 'correct': q.correct_answer
        })
    return render(request, 'games/quiz.html', {'questions': questions_data})

@login_required
def submit_quiz(request):
    if request.method == 'POST':
        questions = QuizQuestion.objects.all()
        score = 0
        total = 0
        for q in questions:
            total += 1
            answer = request.POST.get(f'q_{q.id}')
            if answer == q.correct_answer:
                score += 1
        QuizAttempt.objects.create(user=request.user, score=score, total=total)
        pct = int(score/total*100) if total else 0
        return render(request, 'games/quiz_result.html', {'score': score, 'total': total, 'pct': pct})
    return redirect('quiz')
