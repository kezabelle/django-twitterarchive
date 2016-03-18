# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

from twitterarchive.base.management.commands.twitterarchive import \
    TwitterArchiveCommand
from twitterarchive.models import TweetMaker


class Command(TwitterArchiveCommand):
    def get_tweet_handler_class(self):
        return TweetMaker
