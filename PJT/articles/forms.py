from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'movie_name', 'grade']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "댓글을 남겨보세요 💬",
        })
    )
    class Meta:
        model = Comment
        fields = ['content']
