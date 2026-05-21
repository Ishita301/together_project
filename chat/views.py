from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Message

@login_required
def chat_view(request):
    user = request.user
    if not user.is_coupled():
        return redirect('connect_partner')
    partner = user.partner
    messages_qs = Message.objects.filter(
        sender__in=[user, partner], receiver__in=[user, partner]
    ).order_by('created_at')
    Message.objects.filter(receiver=user, is_seen=False).update(is_seen=True)
    return render(request, 'chat/chat.html', {
        'partner': partner, 'messages': messages_qs,
        'user_id': user.id,
    })

@login_required
def send_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        user = request.user
        partner = user.partner
        if not partner:
            return JsonResponse({'error': 'No partner'}, status=400)
        image = request.FILES['image']
        msg = Message.objects.create(
            sender=user, receiver=partner, image=image, message_type='image'
        )
        return JsonResponse({'success': True, 'image_url': msg.image.url})
    return JsonResponse({'error': 'Bad request'}, status=400)
