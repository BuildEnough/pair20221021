from django import forms
from .models import Comment, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'movie_name', 'grade']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = '댓글을 입력해주세요.'
        self.fields['content'].widget.attrs['cols'] = 10
        self.fields['content'].widget.attrs['rows'] = 1