from __future__ import unicode_literals

from django.apps import AppConfig


class MagazinesConfig(AppConfig):
    name = 'magazines'

    def ready(self):
        from magazines import signals