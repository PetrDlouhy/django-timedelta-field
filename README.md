django-timedelta-field
==========================

.. image:: https://drone.io/bitbucket.org/schinckel/django-timedelta-field/status.png

*This is deprecated in favor of Django native DurationField*
-------

PostgreSQL can store data as INTERVAL type, which is close to meaning the
same as python's timedelta object (although better in a couple of ways).

I have lots of use for timedelta objects, and having code that basically
wrapped integer objects as a number of seconds was common. This module
combines the two:

    * a timedelta.TimedeltaField() object that transparently converts
      to and from datetime.timedelta

    * storage of the data as an INTERVAL in PostgreSQL, or a string in
      other databases. (Other databases will be considered if I ever
      use them, or receive patches).

The coolest part of this package is the way it manipulates strings entered
by users, and presents them. Any string of the format:

    [X weeks,] [Y days,] [Z hours,] [A minutes,] [B seconds]

will be converted to a timedelta object. Even shortened versions can be used:
hrs, hr or h will also suffice.  The parsing ignores trailing 's', but is
smart about adding them in when presenting the data to the user.

To use, install the package, and use the field::

    from django.db import models
    import timedelta

    class MyModel(models.Model):
        the_timedelta = timedelta.fields.TimedeltaField()

There are also some useful methods in helpers.py to work with timedelta
objects. (eg, multiply, divide, modulo and percentages).

Additionally, there are two template filters, `timedelta` and `iso8601`, which
will convert a timedelta object into a valid string.

Examples
-------------

Event model::

    from django.db import models
    import timedelta

    class Event(models.Model):
        start = models.DateTimeField()
        duration = timedelta.fields.TimedeltaField()

        @property
        def finish(self):
            return self.start + self.duration

Storing data within the field::

    evt = Event.objects.create(
        start=datetime.datetime.now(),
        duration=datetime.timedelta(hours=1)
    )
    print evt.finish

    evt.duration = datetime.timedelta(minutes=3)
    print evt.finish

    # We can use valid strings of the format described above.
    Event.objects.update(duration='2 hours, 45 minutes')

    evt = Event.objects.get(pk=evt.pk)
    print evt.finish

    # We can also assign directly to this field a valid string.
    evt.duration = '3 days, 2 hours'
    evt.save()

    # Note: we need to re-fetch to ensure conversion to timedelta
    evt = Event.objects.get(pk=evt.pk)
    print evt.finish

Using with a form.
~~~~~~~~~~~~~~~~~~~~

You can just use a ModelForm, and it will automatically select the
``TimedeltaFormField``, which will handle the conversion between
formatted strings and timedelta objects.

Or you may use the form field directly::

    from django import forms
    import timedelta

    class EventForm(forms.Form):
        start = forms.DateTimeField()
        duration = timedelta.forms.TimedeltaFormField()

This form field will display a value in the format::

    2 day, 3 hours, 1 minute

And will parse data from a similar format.

Have a look in tests.py for examples of the form field/widget output.


Helpers
-------

``nice_repr(timedelta, display='long', sep=', ')``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a string of the format:

    "2 weeks, 7 hours, 1 day"

``display`` may be one of the strings 'minimal', 'short' or 'long'.

``iso8601_repr(timedelta, format=None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a string of the format:

    "P2WT7H1D"

As per ISO8601. For timedeltas less than a whole day, the 'alt' format is supported:

    "PT01:02:03"


``parse(string)``
~~~~~~~~~~~~~~~~~
Parse a string from the ``nice_repr`` formats.


``divide(timedelta, other)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Allow dividing one timedelta by another, or by an integer, float or decimal value.


``modulo(timedelta, other)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Allows modulo division of one timedelta by another, or by an integer.

``percentage(timedelta, timedelta)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Returns what percentage of the first timedelta the second is, as a float.

``decimal_percentag(timedelta, timedelta)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Returns what percentage of the first timedelta the second is, as a decimal.


``multiply(timedelta, other)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Allows for the multiplication of timedeltas by numbers.

``round_to_nearest(obj, timedelta)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Round the first argument (which must be a datetime, time, or timedelta object), to the nearest interval of the second argument.

``decimal_hours(timedelta)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Return a decimal value of the number of hours that this timedelta object refers to.

``total_seconds(timedelta)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A wrapper for python < 2.7's lack of ``timedelta.total_seconds()``

Todo
-------------

Parse ISO8601 strings. Thanks to Guillame Libersat, we can generate them.

Handle strings with times in other languages. I'm not really sure about how
to do this, but it may be useful.

Changelog
----------

0.7.3: Bugfixes/more testing.
       Add alternative format for ISO8601 display: PT00:15:00, for instance.
			 Note that values > timedelta(1) may not be displayed in this manner.

0.7.2: Make nice_repr behave in a more meaningful way with timedelta(0).
			 Thanks to Andy Evan for the report, and Jake Teton-Landis for the fix.

0.7.1: Allow using arbitrary php-style strings in the timedelta template
			 tag argument. Like django's date and time filters.

0.7.0: Support for django 1.5

0.6.7: Added LICENSE file.

0.6.6: Add in a couple of new template filters: total_seconds, and total_seconds_sort.
       The latter zero-pads the value to 10 places, ideal for lexical sorting.
       This correctly sorts timedeltas of up to around 10 years, if you need more
       you can pass an argument to the filter.

0.6.5: Empty string values in database now are returned as None for the field value.
       Note that you must have field.null=True to store a NULL in the db.
       I'm still not 100% happy with this: postgres may choke on empty string values when doing INTERVAL comparisons.
       Thanks to Gustavo Dias jaimes and reidpr for the report/fix.

0.6.4: Correctly parse '1w' (previously required 1wk).
       Don't parse things like '1 hs', require '1 hrs'.
       Test a bit harder.

0.6.3: Correctly parse '1h' as one hour (previously required 1hr).

0.6.2: Remember to include VERSION number.

0.6.0: Added total_seconds helper (for python < 2.7)

0.5.3: Include long_description from this file.

0.5.2: Added ``decimal_percentage``, which gives us a ``decimal.Decimal`` object.

0.5.1: Bugfixes from Mike Fogel.

0.5: Feature from Guillaume Libersat: helper and template for ISO8601 representation.
     Bugfix from croepha: allow for non-plural 'days' string.
     Bugfix from Guillaume Libersat: don't explode if initial is None


0.4.7: Bugfix from savemu: use unicode() instead of str()

0.4.6: Add in support for PostGIS database.
	Make it easier to add in other column types for other databases.

0.4.5: Restore functionality for django <1.2 (thanks Yoav Aner).

0.4.3: Added helpers.modulo, to allow remainder division of timedlelta objects.

0.4.1: changed get_db_prep_value() code to be in get_prep_value(), since I
    was calling it in get_default(), without a connection value.

0.4: added the connection and prepared arguments to get_db_prep_value(),
    so that django 1.3+ will not complain of DeprecationWarnings.
