from django import forms
from .models import Thread, Posts


class ThreadForm(forms.ModelForm):

    # If we want a normal thread, we don't want to show the other fields in
    # the form, and we also want to avoid creating a Poll object or any of its
    # dependent classes if we don't need any. We should only show the relevant
    # fields when we actually want to create a poll.  To handle this we add is_a_poll.
    # Its is set to False therefore will only be included in the POST if it is checked.
    name = forms.CharField(label="Thread name")
    is_a_poll = forms.BooleanField(label="Include a poll?", required=False)

    class Meta:
        model = Thread
        fields = ['name']


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['comment']
