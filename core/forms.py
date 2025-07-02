# forms.py
from django import forms
from .models import File, ProblemCategory, Ticket
from django.contrib.auth.models import User
from .models import Profile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title', 'description', 'category', 'access_level', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter file title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a brief description',
                'rows': 3
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'access_level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'brts_unit': forms.Select(attrs={'class': 'form-control'}),
            'problem_category': forms.Select(attrs={'class': 'form-control'}),
            'terminal': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'responsible': forms.Select(attrs={'class': 'form-control'}),
            'created_by': forms.HiddenInput(),
            'assigned_to': forms.HiddenInput(),
            'created_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'readonly': True}, format='%Y-%m-%dT%H:%M'),
            'updated_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'readonly': True}, format='%Y-%m-%dT%H:%M'),
        }



class ProblemCategoryForm(forms.ModelForm):
    class Meta:
        model = ProblemCategory
        fields = ['brts_unit', 'name']
        widgets = {
            'brts_unit': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
        }