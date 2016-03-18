# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from twitterarchive.base.admin import TweetAdminBase, TweetAuthorAdminBase, \
    TweetURLAdminBase, TweetHashtagAdminBase, TweetMentionAdminBase, \
    TweetMediaAdminBase


class TweetAdmin(TweetAdminBase):
    pass


class TweetAuthorAdmin(TweetAuthorAdminBase):
    pass


class TweetURLAdmin(TweetURLAdminBase):
    pass


class TweetHashtagAdmin(TweetHashtagAdminBase):
    pass


class TweetMentionAdmin(TweetMentionAdminBase):
    pass


class TweetMediaAdmin(TweetMediaAdminBase):
    pass
