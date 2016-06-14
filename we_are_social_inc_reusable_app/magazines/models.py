# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone


class Magazine(models.Model):
    """
    Setup magazine db tables
    """
    name = models.CharField(max_length=254, default='')
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)  # cost of monthly subscription

    def __unicode__(self):
        return self.name


class Purchase(models.Model):
    """
    Lets us link magazines to users and also helps us tell if a subscription
    is valid.
    Define a one-to-many relationship for our user and magazine.
    Use the related_name option on our user, so that when we want to look
    into the user’s purchase, we can type user.purchases instead of
    user.purchases_set.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='purchases')
    magazine = models.ForeignKey(Magazine)
    subscription_end = models.DateTimeField(default=timezone.now)
