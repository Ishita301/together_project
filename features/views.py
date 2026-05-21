from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import OpenWhenMessage, MoodHistory, DateIdea, Notification
import random

@login_required
def open_when_list(request):
    user = request.user
    if not user.is_coupled():
        return redirect('connect_partner')
    received = OpenWhenMessage.objects.filter(for_partner=user)
    created = OpenWhenMessage.objects.filter(created_by=user)
    return render(request, 'features/open_when_list.html', {'received': received, 'created': created})

@login_required
def open_when_create(request):
    if request.method == 'POST':
        occasion = request.POST.get('occasion', '')
        content = request.POST.get('content', '')
        if occasion and content and request.user.partner:
            OpenWhenMessage.objects.create(
                created_by=request.user,
                for_partner=request.user.partner,
                occasion=occasion,
                content=content
            )
            Notification.objects.create(
                user=request.user.partner,
                title='💌 New Open When Message!',
                message=f'A new message is waiting for you: "Open when {occasion}"',
                notif_type='open_when'
            )
            messages.success(request, 'Message created! 💌')
            return redirect('open_when_list')
    return render(request, 'features/open_when_create.html')

@login_required
def open_when_read(request, pk):
    msg = get_object_or_404(OpenWhenMessage, pk=pk, for_partner=request.user)
    if not msg.is_opened:
        msg.is_opened = True
        from django.utils import timezone
        msg.opened_at = timezone.now()
        msg.save()
    return render(request, 'features/open_when_read.html', {'msg': msg})

@login_required
def date_ideas(request):
    ideas = list(DateIdea.objects.all())
    category = request.GET.get('category', '')
    if category:
        ideas = [i for i in ideas if i.category == category]
    random_idea = random.choice(ideas) if ideas else None
    return render(request, 'features/date_ideas.html', {'ideas': ideas, 'random_idea': random_idea, 'category': category})

@login_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user)
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'features/notifications.html', {'notifications': notifs})

@login_required
def mood_history(request):
    history = MoodHistory.objects.filter(user=request.user).order_by('-created_at')[:30]
    return render(request, 'features/mood_history.html', {'history': history})
