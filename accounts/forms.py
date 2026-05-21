from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'nickname', 'bio', 'avatar', 'couple_since', 'anniversary', 'next_meeting', 'theme_preference']
        widgets = {
            'couple_since': forms.DateInput(attrs={'type': 'date'}),
            'anniversary': forms.DateInput(attrs={'type': 'date'}),
            'next_meeting': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class CoupleConnectForm(forms.Form):
    invite_code = forms.CharField(max_length=36, label='Partner Invite Code')
