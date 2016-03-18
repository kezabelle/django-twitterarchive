django-twitterarchive 0.1.0
===========================

Because Twitter is dumb and you can only get the last 3,200 tweets via the API,
as far as I know.

But you can get all of them if you download a stupid "archive" zip file ...
and then parse the JavaScript (which is not quite valid JSON) ...

Installation
------------

First up, you need to clone it.

Once that's downloaded, add the package to your ``INSTALLED_APPS``
in your settings::

    INSTALLED_APPS = (
        # ...
        'twitterarchive.apps.TwitterArchiveConfig',
        # ...
    )

do a migrate::

    python manage.py migrate twitterarchive

Then you can do::

  python manage.py twitterarchive /directory/containing/javascript/files

where the path is, having unzipped your archive, something like
``data/js/tweets`` and contains a bunch of files like
``2009_03.js``, ``2014_12.js`` etc.

You'll end up with a bunch of data in your database, if you're lucky. Most of it
correct.
