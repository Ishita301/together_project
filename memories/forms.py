from django import forms
from .models import Memory

class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ['title', 'caption', 'image', 'video_url', 'memory_date', 'category', 'tags']
        widgets = {
            'memory_date': forms.DateInput(attrs={'type': 'date'}),
            'caption': forms.Textarea(attrs={'rows': 3}),
        }
