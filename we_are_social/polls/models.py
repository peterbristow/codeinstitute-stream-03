from __future__ import unicode_literals

from django.db import models
from django.conf import settings
# Thread is main parent of all poll models
from threads.models import Thread


class Poll(models.Model):
    """
    To store a poll name
    Thread is main parent of all poll models.  Each poll is created inside a
    thread so people can cast their votes and also discuss the subjects as the
    poll proceeds. So create a one-to-one relationship between the thread and
    the poll.
    The poll should be able to access the subjects as well as the votes. This
    is so we can easily access the subjects when rendering our page. We can then
    easily count up the total votes for a poll if the poll is linked to all votes
    with its subjects
    Also, subjects should be related to our votes in addition to the poll, so
    that we can also make a simple call to Django's DRM system, and get how
    many votes each subject has received.
    """
    question = models.TextField()
    thread = models.OneToOneField(Thread, null=True)

    def __unicode__(self):
        return self.question


class PollSubject(models.Model):
    """
    To store what options are available to be voted on in our poll
    """
    name = models.CharField(max_length=255)
    # one poll to many subjects
    poll = models.ForeignKey(Poll, related_name='subjects')

    def __unicode__(self):
        return self.name


class Vote(models.Model):
    """
    To store the votes, so we can do a count up later when showing
    which subject is most popular, etc.
    Data in one place to help with counting and checking of data.
    """
    poll = models.ForeignKey(Poll, related_name='votes')
    subject = models.ForeignKey(PollSubject, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes')
