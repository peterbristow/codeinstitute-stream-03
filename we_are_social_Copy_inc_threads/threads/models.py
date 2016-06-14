from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.conf import settings


class Subject(models.Model):

    name = models.CharField(max_length=255)
    # comes packaged with django-tinymce. It enables our field to render the
    # WYSIWYG editor in our admin.
    description = HTMLField()

    def __unicode__(self):
        return self.name


class Thread(models.Model):
    name = models.CharField(max_length=255)
    # thread is owned by one user.
    # Related_name='threads' is instead of thread_set which gets all threads
    # that are owned be user for example.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='threads')
    # thread belongs to one subject category, but there is more than one subject
    subject = models.ForeignKey(Subject, related_name='threads')
    created_at = models.DateTimeField(default=timezone.now)


class Posts(models.Model):
    # many posts to one single thread
    thread = models.ForeignKey(Thread, related_name='posts')
    # enable field to use tinymce on forum pages.
    comment = HTMLField(blank=True)
    # user who created the/many post
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)
