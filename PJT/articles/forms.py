from django import forms
from .models import Review, Comment, Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"
        labels = {
            'jenre': 'Genre',
        }
        widgets = {
            "runningtime": forms.NumberInput(
                attrs={
                    "maxlength": "3",
                    "min": "1",
                }
            ),
            "releasedate": forms.DateInput(
                format=("%m/%d/%Y"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a date",
                    "type": "date",
                },
            ),
        }


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
