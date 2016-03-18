# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.template.defaultfilters import linebreaksbr
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from ttp.ttp import HASHTAG_EXP


class RetweetFilter(SimpleListFilter):
    parameter_name = 'retweet'
    title = _("tweet type")

    def lookups(self, request, model_admin):
        yield ('1', _("non-retweets"))
        yield ('2', _("retweets"))

    def queryset(self, request, queryset):
        value = self.value()
        if value == '2':
            return queryset.retweets()
        elif value == '1':
            return queryset.non_retweets()


class ReplyFilter(SimpleListFilter):
    parameter_name = 'reply'
    title = _("reply")

    def lookups(self, request, model_admin):
        yield ('1', _("replies"))
        yield ('2', _("non-replies"))

    def queryset(self, request, queryset):
        value = self.value()
        if value == '1':
            return queryset.replies()
        elif value == '2':
            return queryset.non_replies()
        return queryset


class HashtagFilter(SimpleListFilter):
    parameter_name = 'hashtag'
    title = _("hashtag")

    def lookups(self, request, model_admin):
        yield ('1', _("contains hashtag"))

    def queryset(self, request, queryset):
        value = self.value()
        if value == '1':
            return queryset.filter(text__regex=HASHTAG_EXP)
        return queryset


class UserFilter(SimpleListFilter):
    parameter_name = 'username'
    title = _("username")

    def lookups(self, request, model_admin):
        author_cls = model_admin.model.user.field.rel.model
        usernames = (author_cls.objects
                     .values_list('id', 'screen_name')
                     .distinct().order_by('screen_name'))
        for userid, username in usernames:
            yield (userid, username)

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(user__id=value)
        return queryset


class TweetAdminBase(admin.ModelAdmin):
    list_display = ['user', 'html', 'created_at']
    date_hierarchy = 'created_at'
    list_filter = [RetweetFilter, ReplyFilter, HashtagFilter, UserFilter]
    ordering = ['-created_at']

    def html(self, obj):
        html_ = obj.text_as_html()
        if "\r" in html_ or "\n" in html_:
            return linebreaksbr(html_, autoescape=False)
        return html_
    html.allow_tags = True
    html.short_description = _("text")


class TweetAuthorAdminBase(admin.ModelAdmin):
    list_display = ['screen_name', 'name']


class TweetURLAdminBase(admin.ModelAdmin):
    list_display = ['expanded_url', 'url', 'display_url']


class TweetHashtagAdminBase(admin.ModelAdmin):
    list_display = ['text']


class TweetMentionAdminBase(admin.ModelAdmin):
    list_display = ['screen_name', 'name']


class TweetMediaAdminBase(admin.ModelAdmin):
    list_display = ['url', 'media_url', 'inline']
    readonly_fields = ['inline_large']

    def inline(self, obj, height=5):
        return '<img src="%s" style="max-height:%drem;">' % (obj.media_url_https, height)
    inline.allow_tags = True
    inline.short_description = _("Media")
    inline.admin_order_field = 'media_url'

    def inline_large(self, obj):
        return self.inline(obj=obj, height=25)
    inline_large.allow_tags = True
    inline_large.short_description = _("Media")
