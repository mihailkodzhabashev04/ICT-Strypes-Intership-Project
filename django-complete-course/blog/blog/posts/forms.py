from .models import Post, Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post', 'comment_date', 'user']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }