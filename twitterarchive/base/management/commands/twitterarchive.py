# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import json

import os
from django.core.management.base import BaseCommand, CommandError


def chomp_json(data):
    if len(data) > 0 and data[0].strip().startswith('Grailbird.data.tweets'):
        return data[1:]
    return data


class TwitterArchiveCommand(BaseCommand):
    help = 'Closes the specified poll for voting'

    def get_tweet_handler_class(self):
        raise NotImplementedError("Subclasses should implement this to return "
                                  "an appropriate class for building a tweet "
                                  "from a dictionary")

    def add_arguments(self, parser):
        parser.add_argument('dir', nargs='+', type=str)

    def handle(self, **options):
        directories = options.pop('dir', ())
        found_tweets = []
        for directory in directories:
            dir_tweets = self.get_tweets_in_directory(directory=directory)
            dir_tweets = list(dir_tweets)
            found_tweets.extend(dir_tweets)
        if len(found_tweets) < 1:
            raise CommandError("Couldn't find any tweets")
        self.stdout_tweets_found(tweets=found_tweets)
        self.handle_tweets(found_tweets)

    def stdout_tweets_found(self, tweets):
        style = self.style.HTTP_SUCCESS
        write = self.stdout.write
        write(style('Found %(count)d tweets' % {
            'count': len(tweets),
        }))

    def stdout_files_in_directory(self, directory, files):
        # import pdb; pdb.set_trace()
        style = self.style.NOTICE
        write = self.stdout.write
        write(style('Found %(count)d files in %(path)s' % {
            'path': directory,
            'count': len(files),
        }))

    def stdout_tweets_in_file(self, directory, file_, whole_path):
        # import pdb; pdb.set_trace()
        style = self.style.NOTICE
        write = self.stdout.write
        write(style('Successfully processed %(path)s' % {
            'path': whole_path,
        }))

    def stdout_tweet_of_tweets(self, index, tweet_count, result):
        # import pdb; pdb.set_trace()
        style = self.style.NOTICE
        write = self.stdout.write
        created = len(tuple(x[1] for x in result if x[1] is True))
        existed = len(tuple(x[1] for x in result if x[1] is False))
        write(style('Handled %(index)s of %(count)d '
                    '(%(created)d creates, %(updates)d found)' % {
            'index': str(index).zfill(len(str(tweet_count))),
            'count': tweet_count,
            'created': created,
            'updates': existed,
        }))

    def handle_tweets(self, tweets):
        cls = self.get_tweet_handler_class()
        tweet_count = len(tweets)
        for index, tweet in enumerate(tweets):
            handler = cls(tweet)
            result = handler.create()
            self.stdout_tweet_of_tweets(index, tweet_count, result)


    def get_tweets_in_directory(self, directory):
        files = os.listdir(directory)
        js_files = tuple(x for x in files if os.path.splitext(x)[1] == '.js')
        self.stdout_files_in_directory(directory=directory, files=js_files)
        for js_file in js_files:
            js_path = os.path.join(directory, js_file)
            with open(js_path, 'rb') as f:
                tweets = chomp_json(f.readlines())
                flattened = "\n".join(tweets)
                self.stdout_tweets_in_file(directory=directory,
                                           file_=js_file,
                                           whole_path=js_path)
                for tweet in json.loads(flattened):
                    yield tweet
