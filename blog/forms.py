from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user_name', 'user_email', 'content']
        exclude = ['post']
        labels = {
            'user_name': 'Your Name',
            'user_email': 'Your Email',
            'content': 'Your Comment'
        }
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }