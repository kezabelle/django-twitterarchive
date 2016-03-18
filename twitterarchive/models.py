# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from collections import namedtuple

from django.db.models import ForeignKey
from django.utils.encoding import python_2_unicode_compatible
from .base.models import TweetAuthorBase, TweetBase, TweetURLBase, \
    TweetHashtagBase, TweetMediaBase, TweetMentionBase, TweetMakerBase


class TweetAuthor(TweetAuthorBase):
    pass


TweetEntities = namedtuple('TweetEntites', 'user_mentions media hashtags urls')


class Tweet(TweetBase):
    user = ForeignKey(TweetAuthor)

    def get_entities_class(self):
        return TweetEntities

    def from_dict(self, raw_tweet):
        return TweetMaker(raw_tweet=raw_tweet)


class TweetURL(TweetURLBase):
    tweet = ForeignKey(Tweet, related_name='entity_urls_set')

class TweetHashtag(TweetHashtagBase):
    tweet = ForeignKey(Tweet, related_name='entity_hashtags_set')

class TweetMedia(TweetMediaBase):
    tweet = ForeignKey(Tweet, related_name='entity_media_set')

class TweetMention(TweetMentionBase):
    tweet = ForeignKey(Tweet, related_name='entity_mention_set')


class TweetMaker(TweetMakerBase):
    def get_author_class(self):
        return TweetAuthor

    def get_hashtag_class(self):
        return TweetHashtag

    def get_media_class(self):
        return TweetMedia

    def get_mention_class(self):
        return TweetMention

    def get_url_class(self):
        return TweetURL

    def get_tweet_class(self):
        return Tweet
