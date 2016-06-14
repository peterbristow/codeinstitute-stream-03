from django import forms
from .models import Post


class BlogPostForm(forms.ModelForm):

    class Meta:
        model = Post  # tie the form to post model to get its data types
        fields = ('title', 'content', 'image')
