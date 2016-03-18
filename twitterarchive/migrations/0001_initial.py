# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False, help_text='', db_column='id')),
                ('source', models.CharField(max_length=255, help_text='')),
                ('in_reply_to_user_id', models.PositiveIntegerField(blank=True, null=True, help_text='')),
                ('text', models.CharField(max_length=255, help_text='')),
                ('id', models.BigIntegerField(help_text='', db_column='tweet_id')),
                ('in_reply_to_status_id', models.BigIntegerField(blank=True, null=True, help_text='')),
                ('created_at', models.DateTimeField(help_text='')),
                ('in_reply_to_screen_name', models.CharField(max_length=15, help_text='')),
                ('retweeted_status', models.OneToOneField(blank=True, null=True, help_text='', to='twitterarchive.Tweet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TweetAuthor',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False, help_text='', db_column='id')),
                ('name', models.CharField(max_length=255, help_text='')),
                ('screen_name', models.CharField(max_length=15, help_text='')),
                ('protected', models.BooleanField(help_text='')),
                ('id', models.PositiveIntegerField(help_text='', db_column='user_id')),
                ('profile_image_url_https', models.URLField(help_text='')),
                ('verified', models.BooleanField(help_text='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TweetHashtag',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False, help_text='', db_column='id')),
                ('text', models.CharField(max_length=255, help_text='')),
                ('indices', models.CommaSeparatedIntegerField(max_length=255, help_text='')),
                ('tweet', models.ForeignKey(help_text='', related_name='entity_hashtags_set', to='twitterarchive.Tweet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TweetMedia',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False, help_text='', db_column='id')),
                ('expanded_url', models.URLField(help_text='')),
                ('indices', models.CommaSeparatedIntegerField(max_length=255, help_text='')),
                ('url', models.URLField(help_text='')),
                ('media_url', models.URLField(help_text='')),
                ('media_url_https', models.URLField(help_text='')),
                ('id', models.BigIntegerField(help_text='', db_column='media_id')),
                ('display_url', models.URLField(help_text='')),
                ('tweet', models.ForeignKey(help_text='', related_name='entity_media_set', to='twitterarchive.Tweet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TweetMention',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False, help_text='', db_column='id')),
                ('name', models.CharField(max_length=255, help_text='')),
                ('screen_name', models.CharField(max_length=15, help_text='')),
                ('id', models.PositiveIntegerField(help_text='', db_column='user_id')),
                ('indices', models.CommaSeparatedIntegerField(max_length=255, help_text='')),
                ('tweet', models.ForeignKey(help_text='', related_name='entity_mention_set', to='twitterarchive.Tweet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TweetURL',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False, help_text='', db_column='id')),
                ('expanded_url', models.URLField(help_text='')),
                ('display_url', models.URLField(help_text='')),
                ('url', models.URLField(help_text='')),
                ('indices', models.CommaSeparatedIntegerField(max_length=255, help_text='')),
                ('tweet', models.ForeignKey(help_text='', related_name='entity_urls_set', to='twitterarchive.Tweet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='tweet',
            name='user',
            field=models.ForeignKey(help_text='', to='twitterarchive.TweetAuthor'),
        ),
    ]
