from django import forms
from models import Poll, PollSubject


class PollForm(forms.ModelForm):

    # 'label=' renames the label for question to 'What is ...'
    question = forms.CharField(label="What is your poll about?")

    class Meta:
        model = Poll
        fields = ['question']


class PollSubjectForm(forms.ModelForm):
    name = forms.CharField(label="Poll subject name", required=True)

    def __init__(self, *args, **kwargs):
        # override __init__ so that the 'empty_permitted' validation option is
        # set to False as formsets allow empty fields by default.
        super(PollSubjectForm, self).__init__(*args, **kwargs)

        self.empty_permitted = False

    class Meta:
        model = PollSubject
        fields = ['name']
