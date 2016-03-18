# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class TwitterArchiveConfig(AppConfig):
    name = 'twitterarchive'
    verbose_name = _("twitter archive")


    def ready(self):
        from .admin import TweetAdmin, TweetAuthorAdmin, TweetURLAdmin, \
            TweetHashtagAdmin, TweetMentionAdmin, TweetMediaAdmin
        from .models import Tweet, TweetAuthor, TweetURL, \
            TweetHashtag, TweetMention, TweetMedia
        from django.contrib import admin
        admin.site.register(Tweet, TweetAdmin)
        admin.site.register(TweetAuthor, TweetAuthorAdmin)
        admin.site.register(TweetURL, TweetURLAdmin)
        admin.site.register(TweetHashtag, TweetHashtagAdmin)
        admin.site.register(TweetMention, TweetMentionAdmin)
        admin.site.register(TweetMedia, TweetMediaAdmin)
