from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'content',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields  = ('content',)

    content = forms.CharField(
        label = 'write comment ▼',
        widget = forms.TextInput(
            attrs = {
                'placeholder' : '내용을 입력해주세요'
            }
        )
    )