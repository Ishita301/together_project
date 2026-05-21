from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Memory
from .forms import MemoryForm

@login_required
def memory_list(request):
    user = request.user
    if not user.is_coupled():
        return redirect('connect_partner')
    memories = Memory.objects.filter(created_by__in=[user, user.partner])
    category = request.GET.get('category', '')
    if category:
        memories = memories.filter(category=category)
    return render(request, 'memories/memory_list.html', {
        'memories': memories, 
        'category': category,
        'categories': Memory.CATEGORY_CHOICES
    })

@login_required
def memory_create(request):
    form = MemoryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        memory = form.save(commit=False)
        memory.created_by = request.user
        memory.save()
        messages.success(request, 'Memory saved! 📸')
        return redirect('memory_list')
    return render(request, 'memories/memory_form.html', {'form': form, 'title': 'New Memory'})

@login_required
def memory_detail(request, pk):
    user = request.user
    memory = get_object_or_404(Memory, pk=pk)
    if not user.is_coupled() or memory.created_by not in [user, user.partner]:
        return redirect('memory_list')
    return render(request, 'memories/memory_detail.html', {'memory': memory})

@login_required
def memory_delete(request, pk):
    memory = get_object_or_404(Memory, pk=pk, created_by=request.user)
    if request.method == 'POST':
        memory.delete()
        messages.success(request, 'Memory deleted.')
    return redirect('memory_list')

@login_required
def toggle_favorite(request, pk):
    user = request.user
    memory = get_object_or_404(Memory, pk=pk)
    memory.is_favorite = not memory.is_favorite
    memory.save()
    return JsonResponse({'is_favorite': memory.is_favorite})
