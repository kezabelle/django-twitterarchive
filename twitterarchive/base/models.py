# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db.models import Model, CharField, PositiveIntegerField, \
    BigIntegerField, DateTimeField, BooleanField, URLField, \
    AutoField, CommaSeparatedIntegerField, OneToOneField, QuerySet
from django.utils.encoding import python_2_unicode_compatible
from ttp import ttp


class TweetMentionBase(Model):
    _id = AutoField(primary_key=True, db_column='id')
    name = CharField(max_length=255)
    screen_name = CharField(max_length=15)
    id = PositiveIntegerField(db_column='user_id')
    indices = CommaSeparatedIntegerField(max_length=255)

    class Meta:
        abstract = True


class TweetURLBase(Model):
    _id = AutoField(primary_key=True, db_column='id')
    expanded_url = URLField()
    display_url = URLField()
    url = URLField()
    indices = CommaSeparatedIntegerField(max_length=255)

    class Meta:
        abstract = True


class TweetHashtagBase(Model):
    _id = AutoField(primary_key=True, db_column='id')
    text = CharField(max_length=255)
    indices = CommaSeparatedIntegerField(max_length=255)

    class Meta:
        abstract = True


class TweetMediaBase(Model):
    _id = AutoField(primary_key=True, db_column='id')
    expanded_url = URLField()
    indices = CommaSeparatedIntegerField(max_length=255)
    url = URLField()
    media_url = URLField()
    media_url_https = URLField()
    id = BigIntegerField(db_column='media_id')
    display_url = URLField()

    class Meta:
        abstract = True


@python_2_unicode_compatible
class TweetAuthorBase(Model):
    _id = AutoField(primary_key=True, db_column='id')
    name = CharField(max_length=255)
    screen_name = CharField(max_length=15)
    protected = BooleanField()
    id = PositiveIntegerField(db_column='user_id')
    profile_image_url_https = URLField()
    verified = BooleanField()

    def __str__(self):
        return self.screen_name

    class Meta:
        abstract = True



class TweetQuerySet(QuerySet):
    def retweets(self):
        return self.filter(retweeted_status__isnull=False)

    def non_retweets(self):
        return self.filter(retweeted_status__isnull=True)

    def replies(self):
        return self.filter(in_reply_to_status_id__isnull=False)

    def non_replies(self):
        return self.filter(in_reply_to_status_id__isnull=True)



@python_2_unicode_compatible
class TweetBase(Model):
    """
    We don't need:
    in_reply_to_status_id_str
    id_str
    in_reply_to_user_id_str
    """
    _id = AutoField(primary_key=True, db_column='id')
    source = CharField(max_length=255)
    # we don't need
    entities = 1
    geo = 1
    in_reply_to_user_id = PositiveIntegerField(null=True, blank=True)
    text = CharField(max_length=255)
    id = BigIntegerField(db_column='tweet_id')
    in_reply_to_status_id = BigIntegerField(null=True, blank=True)
    created_at = DateTimeField()
    in_reply_to_screen_name = CharField(max_length=15)
    retweeted_status = OneToOneField('self', null=True, blank=True)
    objects = TweetQuerySet.as_manager()

    def __str__(self):
        return self.text

    def get_entities_class(self):
        raise NotImplementedError("Concrete subclasses should implement this")

    @property
    def entities(self):
        # should prolly cache this ...
        cls = self.get_entities_class()
        return cls(
            user_mentions=self.entity_mention_set.all(),
            media=self.entity_media_set.all(),
            hashtags=self.entity_hashtags_set.all(),
            urls=self.entity_urls_set.all(),
        )

    def parse(self):
        parser = ttp.Parser()
        return parser.parse(self.text)

    def text_as_html(self):
        return self.parse().html


    class Meta:
        abstract = True


class TweetMakerBase(object):
    __slots__ = (
        'entities',
        'user_mentions',
        'media',
        'hashtags',
        'urls',
        'geo',
        'user',
        'tweet',
    )
    def __init__(self, raw_tweet):
        self.entities = raw_tweet.pop('entities', {})
        mentions = self.entities.pop('user_mentions', {})
        for mention in mentions:
            mention.pop('id_str', None)
        self.user_mentions = mentions
        medias = self.entities.pop('media', {})
        for media in medias:
            media.pop('id_str', None)
            media.pop('sizes', None)
        self.media = medias
        self.hashtags = self.entities.pop('hashtags', {})
        self.urls = self.entities.pop('urls', {})
        self.geo = raw_tweet.pop('geo', {})
        self.user = raw_tweet.pop('user', {})
        self.user.pop('id_str', None)
        raw_tweet.pop('id_str', None)
        raw_tweet.pop('in_reply_to_status_id_str', None)
        raw_tweet.pop('in_reply_to_user_id_str', None)
        raw_tweet['created_at'] = raw_tweet['created_at'].rpartition('+')[0].strip()
        self.tweet = raw_tweet

    def get_tweet_class(self):
        raise NotImplementedError("Subclasses should implement this")

    def get_author_class(self):
        raise NotImplementedError("Subclasses should implement this")

    def get_mention_class(self):
        raise NotImplementedError("Subclasses should implement this")

    def get_media_class(self):
        raise NotImplementedError("Subclasses should implement this")

    def get_hashtag_class(self):
        raise NotImplementedError("Subclasses should implement this")

    def get_url_class(self):
        raise NotImplementedError("Subclasses should implement this")

    def create(self):
        if 'retweeted_status' in self.tweet:
            retweet_of = self.tweet.pop('retweeted_status', {})
            rt = self.__class__(raw_tweet=retweet_of)
            result = rt.create()
            self.tweet['retweeted_status'] = result[1][0]

        tweet_cls = self.get_tweet_class()
        author_cls = self.get_author_class()
        mention_cls = self.get_mention_class()
        media_cls = self.get_media_class()
        hashtag_cls = self.get_hashtag_class()
        url_cls = self.get_url_class()

        created = []
        author = None
        if self.user:
            result = author_cls.objects.get_or_create(**self.user)
            author = result[0]
            created.append(result)
        tweet_result = tweet_cls.objects.get_or_create(**dict(user=author, **self.tweet))
        created.append(tweet_result)
        tweet = tweet_result[0]

        if self.user_mentions:
            mentions = [mention_cls.objects.get_or_create(**dict(tweet=tweet, **x))
                        for x in self.user_mentions]
            created.extend(mentions)

        if self.media:
            created.extend([media_cls.objects.get_or_create(**dict(tweet=tweet, **x))
                            for x in self.media])
        if self.hashtags:
            created.extend([hashtag_cls.objects.get_or_create(**dict(tweet=tweet, **x))
                            for x in self.hashtags])
        if self.urls:
            created.extend([url_cls.objects.get_or_create(**dict(tweet=tweet, **x))
                            for x in self.urls])
        return created
