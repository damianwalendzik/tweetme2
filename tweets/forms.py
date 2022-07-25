from unittest.util import _MAX_LENGTH
from django import forms
from .models import Tweet

_MAX_TWEET_LENGTH = 240

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        content=self.cleaned_data.get('content')
        if len(content) > _MAX_TWEET_LENGTH:
            raise forms.ValidationError('The message is too long')
        return content
        