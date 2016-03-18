# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class TwitterArchiveConfig(AppConfig):
    name = 'twitterarchive'
    verbose_name = _("twitter archive")


    def ready(self):
        from .admin import TweetAdmin
        from .models import Tweet
        from django.contrib import admin
        admin.site.register(Tweet, TweetAdmin)
