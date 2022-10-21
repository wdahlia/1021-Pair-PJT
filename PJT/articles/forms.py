from django import forms
from .models import Review, Comment, Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "title",
            "content",
            "grade",
        ]
        widgets = {
            "grade": forms.NumberInput(
                attrs={
                    "maxlength": "1",
                    "max": "10",
                    "min": "1",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "댓글을 남겨보세요 💬",
            }
        ),
    )

    class Meta:
        model = Comment
        fields = [
            "content",
        ]
