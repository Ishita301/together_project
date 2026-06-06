# games/views.py
# FIXED: Uses correct model names from your actual DB:
#   - TruthOrDare (games app) for truth/dare
#   - ThisOrThatQuestion + ThisOrThatAnswer (games app)
#   - QuizQuestion + QuizAttempt (games app)
#   - DateIdea (features app)
#   - BucketListItem (games app)

import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

from .models import (
    TruthOrDare, ThisOrThatQuestion, ThisOrThatAnswer,
    QuizQuestion, QuizAttempt, BucketListItem
)
from features.models import DateIdea


# ─────────────────────────────────────────────────────────────
#  TRUTH OR DARE
# ─────────────────────────────────────────────────────────────
@login_required
def truth_dare(request):
    """
    FIXED: Uses TruthOrDare model with type field ('truth'/'dare').
    No-repeat logic: tracks seen IDs in session so questions
    don't repeat until all have been shown.
    """
    td_type  = request.GET.get('type', 'truth')   # 'truth' or 'dare'
    category = request.GET.get('category', 'cute')

    CATEGORIES = [
        ('cute',      'Cute 🌸'),
        ('romantic',  'Romantic 💕'),
        ('funny',     'Funny 😂'),
        ('deep',      'Deep 💭'),
        ('spicy',     'Spicy 🌶️'),
    ]

    # All questions for this type+category
    all_qs = list(
        TruthOrDare.objects.filter(type=td_type, category=category)
                           .values_list('id', 'content')
    )

    if not all_qs:
        return render(request, 'games/truth_dare.html', {
            'item': None,
            'td_type': td_type,
            'category': category,
            'categories': CATEGORIES,
            'remaining': 0,
            'total': 0,
        })

    # Session key tracks which IDs have been seen
    session_key = f'seen_td_{td_type}_{category}'
    seen_ids = set(request.session.get(session_key, []))

    # Find unseen questions
    unseen = [(qid, content) for qid, content in all_qs if qid not in seen_ids]

    # If all seen, reset
    if not unseen:
        seen_ids = set()
        unseen = all_qs
        request.session[session_key] = []

    # Pick one at random
    chosen_id, chosen_content = random.choice(unseen)

    # Mark as seen
    seen_ids.add(chosen_id)
    request.session[session_key] = list(seen_ids)

    # Simple object to pass to template
    class Item:
        def __init__(self, content):
            self.content = content

    return render(request, 'games/truth_dare.html', {
        'item':       Item(chosen_content),
        'td_type':    td_type,
        'category':   category,
        'categories': CATEGORIES,
        'remaining':  len(unseen) - 1,
        'total':      len(all_qs),
    })


# ─────────────────────────────────────────────────────────────
#  THIS OR THAT
# ─────────────────────────────────────────────────────────────
@login_required
def this_or_that(request):
    """
    FIXED: Correct model usage. Shows one random unanswered
    question. Calculates live match % with partner.
    """
    user = request.user

    all_qs    = list(ThisOrThatQuestion.objects.all())
    answered  = set(
        ThisOrThatAnswer.objects.filter(user=user)
                                .values_list('question_id', flat=True)
    )
    unanswered = [q for q in all_qs if q.id not in answered]

    # Pick next question — unanswered first, then random repeat
    if unanswered:
        question = random.choice(unanswered)
    elif all_qs:
        question = random.choice(all_qs)
    else:
        question = None

    my_answer      = None
    partner_answer = None
    match_pct      = 0
    match_count    = 0
    total_compared = 0

    if question:
        my_answer = ThisOrThatAnswer.objects.filter(
            user=user, question=question
        ).first()

        if user.partner:
            partner_answer = ThisOrThatAnswer.objects.filter(
                user=user.partner, question=question
            ).first()

            # Calculate overall match %
            my_ans_map = dict(
                ThisOrThatAnswer.objects.filter(user=user)
                                        .values_list('question_id', 'answer')
            )
            partner_ans_map = dict(
                ThisOrThatAnswer.objects.filter(user=user.partner)
                                        .values_list('question_id', 'answer')
            )
            common_ids = set(my_ans_map) & set(partner_ans_map)
            total_compared = len(common_ids)
            match_count    = sum(
                1 for qid in common_ids
                if my_ans_map[qid] == partner_ans_map[qid]
            )
            match_pct = int(match_count / total_compared * 100) if total_compared else 0

    return render(request, 'games/this_or_that.html', {
        'question':       question,
        'my_answer':      my_answer,
        'partner_answer': partner_answer,
        'match_pct':      match_pct,
        'match_count':    match_count,
        'total_compared': total_compared,
        'answered_total': len(answered),
        'total_qs':       len(all_qs),
    })


@login_required
def answer_tot(request):
    """
    FIXED: AJAX endpoint — saves answer and returns partner's
    answer (if any) so the UI can reveal it instantly.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    q_id   = request.POST.get('question_id')
    answer = request.POST.get('answer')

    if not q_id or answer not in ('A', 'B'):
        return JsonResponse({'error': 'Invalid data'}, status=400)

    question = get_object_or_404(ThisOrThatQuestion, id=q_id)

    ThisOrThatAnswer.objects.update_or_create(
        user=request.user, question=question,
        defaults={'answer': answer}
    )

    # Return partner answer so JS can show match/mismatch immediately
    partner_answer = None
    match = None
    if request.user.partner:
        pa = ThisOrThatAnswer.objects.filter(
            user=request.user.partner, question=question
        ).first()
        if pa:
            partner_answer = pa.answer
            match = (pa.answer == answer)

    return JsonResponse({
        'success':        True,
        'partner_answer': partner_answer,
        'match':          match,
    })


# ─────────────────────────────────────────────────────────────
#  QUIZ
# ─────────────────────────────────────────────────────────────
@login_required
def quiz(request):
    """
    FIXED: Multi-category quiz. Passes shuffled options to template.
    """
    QUIZ_CATEGORIES = [
        ('general',      'How Well Do You Know Me? 🧠'),
        ('relationship', 'Relationship 💑'),
        ('funny',        'Funny 😂'),
        ('favorites',    'Favourites ⭐'),
        ('future',       'Future Plans 🌍'),
    ]

    category  = request.GET.get('category', 'general')
    questions = list(QuizQuestion.objects.filter(category=category).order_by('?')[:10])

    # Shuffle options for each question
    questions_data = []
    for q in questions:
        options = [
            ('A', q.option_a),
            ('B', q.option_b),
            ('C', q.option_c),
            ('D', q.option_d),
        ]
        random.shuffle(options)
        questions_data.append({'obj': q, 'options': options})

    return render(request, 'games/quiz.html', {
        'questions':        questions_data,
        'category':         category,
        'quiz_categories':  QUIZ_CATEGORIES,
    })


@login_required
def submit_quiz(request):
    """
    FIXED: Scores quiz, stores attempt, shows breakdown + leaderboard.
    """
    if request.method != 'POST':
        return redirect('quiz')

    QUIZ_CATEGORIES = [
        ('general',      'How Well Do You Know Me? 🧠'),
        ('relationship', 'Relationship 💑'),
        ('funny',        'Funny 😂'),
        ('favorites',    'Favourites ⭐'),
        ('future',       'Future Plans 🌍'),
    ]

    category   = request.POST.get('category', 'general')
    questions  = QuizQuestion.objects.filter(category=category)

    score          = 0
    total_possible = 0
    results        = []

    for q in questions:
        total_possible += q.points
        user_answer = request.POST.get(f'q_{q.id}')

        # Map letter back to text
        letter_to_text = {
            'A': q.option_a, 'B': q.option_b,
            'C': q.option_c, 'D': q.option_d,
        }
        correct_letter = q.correct_answer
        correct_text   = letter_to_text.get(correct_letter, '')
        is_correct     = (user_answer == correct_letter)

        if is_correct:
            score += q.points

        results.append({
            'question':     q.question,
            'is_correct':   is_correct,
            'correct_text': correct_text,
        })

    attempt = QuizAttempt.objects.create(
        user=request.user,
        score=score,
        total_possible=total_possible,
        category=category,
    )
    pct = attempt.percentage()

    # My personal best for this category
    my_best = QuizAttempt.objects.filter(
        user=request.user, category=category
    ).order_by('-score').first()

    # Partner's best
    partner_best = None
    if request.user.partner:
        partner_best = QuizAttempt.objects.filter(
            user=request.user.partner, category=category
        ).order_by('-score').first()

    return render(request, 'games/quiz_result.html', {
        'score':          score,
        'total':          total_possible,
        'pct':            pct,
        'results':        results,
        'category':       category,
        'quiz_categories': QUIZ_CATEGORIES,
        'my_best':        my_best,
        'partner_best':   partner_best,
    })


# ─────────────────────────────────────────────────────────────
#  DATE IDEAS
# ─────────────────────────────────────────────────────────────
@login_required
def date_ideas(request):
    """
    FIXED: DateIdea is in features app.
    Supports category filter + surprise random pick.
    """
    CATEGORIES = [
        ('virtual',      'Virtual 💻'),
        ('indoor',       'Indoor 🏠'),
        ('outdoor',      'Outdoor 🌿'),
        ('budget',       'Budget 💸'),
        ('longdistance', 'Long Distance 💕'),
        ('rainy',        'Rainy Day 🌧️'),
        ('anniversary',  'Anniversary 💍'),
    ]

    category = request.GET.get('category', '')
    ideas    = DateIdea.objects.all()

    if category:
        ideas = ideas.filter(category=category)

    # Saved IDs for this user
    from features.models import SavedDateIdea
    saved_ids = set(
        SavedDateIdea.objects.filter(user=request.user)
                             .values_list('idea_id', flat=True)
    ) if hasattr(DateIdea, 'saveddateidea_set') else set()

    # Try to load SavedDateIdea safely
    try:
        from features.models import SavedDateIdea as SDI
        saved_ids = set(
            SDI.objects.filter(user=request.user)
                       .values_list('idea_id', flat=True)
        )
    except Exception:
        saved_ids = set()

    # Random / surprise pick
    ideas_list   = list(ideas)
    random_idea  = random.choice(ideas_list) if ideas_list else None

    return render(request, 'games/date_ideas.html', {
        'ideas':       ideas_list,
        'category':    category,
        'categories':  CATEGORIES,
        'random_idea': random_idea,
        'saved_ids':   saved_ids,
    })


@login_required
def save_date_idea(request, pk):
    """AJAX — toggle save/unsave a date idea."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    idea = get_object_or_404(DateIdea, pk=pk)

    try:
        from features.models import SavedDateIdea
        obj, created = SavedDateIdea.objects.get_or_create(
            user=request.user, idea=idea
        )
        if not created:
            obj.delete()
            return JsonResponse({'saved': False})
        return JsonResponse({'saved': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ─────────────────────────────────────────────────────────────
#  BUCKET LIST
# ─────────────────────────────────────────────────────────────
@login_required
def bucket_list(request):
    """Couple shared bucket list."""
    user = request.user
    if not user.is_coupled():
        return redirect('connect_partner')

    items = BucketListItem.objects.filter(
        created_by__in=[user, user.partner]
    ).order_by('is_completed', 'created_at')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            BucketListItem.objects.create(
                created_by=user,
                title=title,
                description=request.POST.get('description', ''),
                category=request.POST.get('category', 'dream'),
                target_date=request.POST.get('target_date') or None,
            )
            messages.success(request, '🌟 Added to your bucket list!')
            return redirect('bucket_list')

    return render(request, 'games/bucket_list.html', {'items': items})


@login_required
def toggle_bucket(request, pk):
    """AJAX — mark bucket list item complete/incomplete."""
    item = get_object_or_404(BucketListItem, pk=pk)
    item.is_completed = not item.is_completed
    item.completed_at = timezone.now() if item.is_completed else None
    item.save()
    return JsonResponse({'is_completed': item.is_completed})