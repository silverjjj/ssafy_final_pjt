from django import forms
from .models import PleaseAdd, MovieRatings, Moviestore

class PleaseAddForm(forms.ModelForm):
    class Meta:
        model = PleaseAdd
        fields = ('movie_request',)


class RateForm(forms.ModelForm):
    class Meta:
        model = MovieRatings
        fields = ('score',)
    
    score = forms.IntegerField(
        max_value = 10,
        min_value = 0,
        label = '평점',
        help_text = '0-10사이의 값으로 입력해주세요. 좋을 수록 큰 수:D',
        widget = forms.NumberInput(
            attrs={
                'placeholder':'☆☆☆☆☆☆☆☆☆☆'
            }
            )

    )


class MoviestoreForm(forms.ModelForm):
    class Meta:
        model = Moviestore
        fields = '__all__'