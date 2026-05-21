from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import User
from .forms import SignupForm, LoginForm, ProfileForm, CoupleConnectForm
from features.models import Notification

def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Welcome to Together, {user.first_name or user.username}! 💕")
        return redirect('dashboard')
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
def dashboard(request):
    user = request.user
    partner = user.partner
    from datetime import date
    today = date.today()
    days_together = None
    anniversary_countdown = None
    next_meeting_countdown = None
    if user.couple_since:
        days_together = (today - user.couple_since).days
    if user.anniversary:
        ann = user.anniversary.replace(year=today.year)
        if ann < today:
            ann = ann.replace(year=today.year + 1)
        anniversary_countdown = (ann - today).days
    if user.next_meeting:
        next_meeting_countdown = (user.next_meeting - today).days
    notifications = Notification.objects.filter(user=user, is_read=False).count()
    context = {
        'user': user, 'partner': partner,
        'days_together': days_together,
        'anniversary_countdown': anniversary_countdown,
        'next_meeting_countdown': next_meeting_countdown,
        'notifications': notifications,
    }
    return render(request, 'dashboard.html', context)

@login_required
def profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile updated! ✨')
        return redirect('profile')
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def connect_partner(request):
    user = request.user
    if user.is_coupled():
        messages.info(request, 'You are already connected with a partner!')
        return redirect('dashboard')
    if request.method == 'POST':
        invite_code = request.POST.get('invite_code', '').strip()
        try:
            partner = User.objects.get(invite_code=invite_code)
            if partner == user:
                messages.error(request, "You can't connect with yourself! 😄")
            elif partner.is_coupled():
                messages.error(request, 'This person is already in a couple.')
            else:
                user.partner = partner
                partner.partner = user
                from datetime import date
                user.couple_since = date.today()
                partner.couple_since = date.today()
                user.save()
                partner.save()
                Notification.objects.create(
                    user=partner,
                    title='💕 New Connection!',
                    message=f'{user.username} connected with you!',
                    notif_type='couple'
                )
                messages.success(request, f'Connected with {partner.username}! 💕')
                return redirect('dashboard')
        except User.DoesNotExist:
            messages.error(request, 'Invalid invite code. Please check and try again.')
    return render(request, 'accounts/connect_partner.html', {'invite_code': user.invite_code})

@login_required
def disconnect_partner(request):
    if request.method == 'POST':
        user = request.user
        partner = user.partner
        if partner:
            partner.partner = None
            partner.save()
        user.partner = None
        user.save()
        messages.info(request, 'Partner disconnected.')
    return redirect('dashboard')

@login_required
def update_mood(request):
    if request.method == 'POST':
        mood = request.POST.get('mood', 'happy')
        mood_message = request.POST.get('mood_message', '')
        request.user.current_mood = mood
        request.user.mood_message = mood_message
        request.user.save()
        from features.models import MoodHistory
        MoodHistory.objects.create(user=request.user, mood=mood, message=mood_message)
        if request.user.partner:
            Notification.objects.create(
                user=request.user.partner,
                title=f'Mood Update 💭',
                message=f'{request.user.username} is feeling {mood}',
                notif_type='mood'
            )
        messages.success(request, 'Mood updated! 💫')
    return redirect('dashboard')
