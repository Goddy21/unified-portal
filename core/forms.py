# forms.py
from django import forms
from .models import File

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