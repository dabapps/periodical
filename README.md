# Periodical

**A library for working with time and date series in Python.**

[![Build Status](https://travis-ci.org/dabapps/periodical.png?branch=master)](https://travis-ci.org/dabapps/periodical)
[![Coverage Status](https://coveralls.io/repos/dabapps/periodical/badge.png?branch=master)](https://coveralls.io/r/dabapps/periodical?branch=master)
[![PyPI version](https://badge.fury.io/py/periodical.png)](http://badge.fury.io/py/periodical)

The `periodical` Python module provides a convienient way of dealing with time and date series.  

These are particular useful for aggregating events at differing time granualities, for example when generating graphs or reports covering a given time span.

### Requirements

`periodical` currently supports Python 2.7, 3.2 and 3.3.

### Installation

You can install the `periodical` module using pip:

    pip install periodical

### An example of using periodical

In this example we have a service which is logging the response times from a web application.  We'd like to generate the average response time for each hourly period over the previous 24 hours.

First we'll get the sequence of the last 24 hour periods.

    >>> import periodical
    >>> hour_periods = periodical.time_periods_descending(span='hour', num_periods=24)
    >>> hour_periods
    [
        <TimePeriod '2014-04-28T15:00Z'>,
        <TimePeriod '2014-04-28T14:00Z'>,
        <TimePeriod '2014-04-28T13:00Z'>,
        ...
    ]

Let's assume we have a list of requests in the `request_log` variable.  Let's also assume that each of the request objects has an asociated `started` property, which is a `datetime` representing the time the request was recieved, and a `duration` property, which is a float representing the number of seconds it took to generate and send a response.

In order to work with this data in periodical we need to first transform our objects into a list of two-tuple data points, of the form `(datetime, value)`, like so:

    >>> data_points = [(request.started, request.duration) for request in request_log]
    >>> data_points
    [
        (datetime.datetime(2014, 4, 28, 15, 23, 35, 682504, tzinfo=<UTC>), 0.24),
        (datetime.datetime(2014, 4, 28, 15, 22, 12, 659191, tzinfo=<UTC>), 0.22),
        (datetime.datetime(2014, 4, 28, 15, 21, 45, 728530, tzinfo=<UTC>), 0.30),
        ...
    ]

Now that we have our data points we can get the average response time within each hour time period.  We use the `periodical.average()` function, which returns an ordered dictionary mapping each time period onto the average value of data points within that period.

    >>> average_response_times = periodical.average(hour_periods, data_points)
    >>> average_response_times
    {
        <TimePeriod '2014-04-28T15:00Z'>: 0.26,
        <TimePeriod '2014-04-28T14:00Z'>: 0.24,
        <TimePeriod '2014-04-28T13:00Z'>: 0.35,
        ...
    }

---

## TimePeriod and DatePeriod objects

The two basic building blocks of periodical are the `TimePeriod` and `DatePeriod` classes.

The `TimePeriod` class is used to represent an interval between two datetimes.

The `DatePeriod` class is used to represent an interval of dates.

### Creating period instances

You can instantiate a `TimePeriod` or `DatePeriod` object by specifying a time span.  By default this will return a period that covers the current time or day in UTC timezone.

For  `DatePeriod` this may be one of `'day'`, `'week'`, `'month'`, `'quarter'` or `'year'`.

    >>> import periodical
    >>> period = periodical.DatePeriod(span='week')
    >>> period
    <DatePeriod '2014-W02'>

For `TimePeriod` this may be any of the date spans, or may also be one of `'hour'`, `'minute'`, or `'second'`.

    >>> period = periodical.TimePeriod(span='hour')
    >>> period
    <TimePeriod '2014-01-02T14Z'>

You can also explicitly provide a date or time that you wish the period to cover.

	>>> date = datetime.date(2015, 1, 25)
    >>> period = periodical.DatePeriod(date=date, span='week')
    >>> period
    <DatePeriod '2015-W04'>

### A note on timezones

The default implementations for `DatePeriod` and `TimePeriod` return periods coverring the current date or time *in the UTC timezone*.  To work with local time you'll need to pass the local date or time explicitly.

For example to get the current week period, using local time to determine the current date instead of using UTC time, we would do the following:

    >>> today = datetime.date.today()
    >>> period = periodical.DatePeriod(date=today, span='week')

#### Timezone awareness and TimePeriod objects

When passing a `datetime` instance to `TimePeriod`, the resulting period instance will use the same timezone info as the provided argument, or be timezone-naive if no timezone info is included.

Instantiating a `TimePeriod` with no timezone information:

	>>> time = datetime.datetime(2015, 1, 25, 4)
    >>> period = periodical.TimePeriod(time=time, span='hour')
    >>> period
    <TimePeriod '2015-01-25T04'>

Instantiating a `TimePeriod` with an explicit UTC timezone:

	>>> time = datetime.datetime(2015, 1, 25, 4, tzinfo=periodical.UTC())
    >>> period = periodical.TimePeriod(time=time, span='hour')
    >>> period
    <TimePeriod '2015-01-25T04Z'>

If not specified, the default time is set using `periodical.utcnow()` which returns the current time with a UTC timezone.

You can determine the timezone information in use by examining the suffix of the `TimePeriod` representation.

    <TimePeriod '2015-01-25T04'>        # 25th Jan 2015, 04:00 Timezone naive
    <TimePeriod '2015-01-25T04Z'>       # 25th Jan 2015, 04:00 UTC
    <TimePeriod '2015-01-25T04-05:00'>  # 25th Jan 2015, 04:00 EST

### Start and end dates

Both objects provide `start` and `end` properties.  For `DatePeriod` objects these return an instance of `date`.

    >>> period = periodical.DatePeriod(span='week')
    >>> period.start
    datetime.date(2014, 1, 6)
    >>> period.end
    datetime.date(2014, 1, 12)

For `TimePeriod` objects these properties return `datetime` instances.

    >>> period = periodical.TimePeriod(span='month')
    >>> period.start
    datetime.datetime(2014, 1, 1, 0, 0, tzinfo=<UTC>)
	>>> period.end
	datetime.datetime(2014, 2, 1, 0, 0, tzinfo=<UTC>)

Period objects also provide a `contains()` method that takes a date or time object and returns `True` if the date is contained by the given period.

    >>> period = periodical.DatePeriod(span='month')
    >>> period.contains(datetime.date(2014, 3, 20))
    True
    >>> period.contains(datetime.date(2014, 4, 20))
    False

### Differences between time and date periods

When considering the end point of a period there is an important distinction to be made between `DatePeriod` and `TimePeriod` objects, due to the fact that dates and times represent fundamentally different concepts.

* A `date` represents a discreet entity.  The `end` property of a `DatePeriod` will be the last date included in that period.
* A `datetime` represents a point in time.  The `end` property of a `TimePeriod` will not be included in that period.

For example, the date and time periods for the month of November 2014 may be represented like so:

    DatePeriod: start date <= period <= end date

             2014-11-01                              2014-11-30
                 |                                       |
                 V                                       V
            +---------+---------+--   --+----------+----------+
            |  1 Nov. |  2 Nov. |       |  29 Nov. |  30 Nov. |
            |  2014   |  2014   |  ...  |   2015   |   2015   |
            +---------+---------+--   --+----------+----------+
            ^                                                 ^
            |                                                 |
    2014-11-01 00:00:00                               2014-12-01 00:00:00
    
    TimePeriod: start time <= period < end time


### Iterating through periods

To return a new `TimePeriod` or `DatePeriod` object that occurs immediately before or after the existing period, you can call the `.next()` and `.previous()` methods.

    >>> period = periodical.DatePeriod(date=datetime.date(2014, 01, 05), span='week')
    >>> period.next()
    <DatePeriod '2014-W02'>
    >>> period.previous()
    <DatePeriod '2013-W52'>

### String representations

DatePeriod objects use a unique representation that follows ISO 8601 with the following exceptions:

* Only the relevant portion of the period will be included in the representation.
* Quarterley intervals use a 'Q' prefix to the quarter.
* If present, then timezone information is included using a `Z` or `±HH:MM` suffix.

The following are all valid representations of `DatePeriod` objects:

    <DatePeriod '2015'>        # The 2015 year.
    <DatePeriod '2013-Q2'>     # The second quarter of 2013.
    <DatePeriod '2014-03'>     # March 2014.
    <DatePeriod '2013-W24'>    # The 24th week of 2013.  (Numbering by ISO 8601 weeks)
    <DatePeriod '2014-04-29'>  # The 29th of April 2014.

The following are all valid representations of `TimePeriod` objects:

    <TimePeriod '2015Z'>       # The 2015 year, UTC.
    <TimePeriod '2013-Q2Z'>    # The second quarter of 2013, UTC.
    <TimePeriod '2014-03'>     # March 2014, timezone-naive.
    <TimePeriod '2013-W24Z'>   # The 24th week of 2013, UTC.  (Numbering by ISO 8601 weeks)
    <TimePeriod '2014-04-29-05:00'>           # The 29th of April 2014, EST.
	<TimePeriod '2014-04-29T15Z'>             # 15:00:00-16:00:00 UTC, 29th of April 2014.
	<TimePeriod '2014-04-29T15:34'>           # 15:34:00-15:35:00 timezone-naive, 29th of April 2014.
	<TimePeriod '2014-04-29T15:34:24-05:00'>  # 15:34:24-15:34:25 EST, 29th of April 2014.

You can also instantiate a `TimePeriod` or `DatePeriod` object using it's unique representation.

    >>> period = periodical.DatePeriod('2014-Q1')
    >>> period.start
    datetime.date(2014, 1, 1)
    >>> period.end
    datetime.date(2014, 3, 31)

The `isoformat()` method returns a valid ISO 8601 formatted time representing the start of the range.  Note that quarterly representations cannot be expressed in ISO 8601, so will simply return the monthly representation of the start date.

    '2015'               # The 2015 year.
    '2013-04'            # The second quarter of 2013.
    '2014-03'            # March, 2014.
    '2013-W24'           # The 24th week of 2013.  (Numbering by ISO 8601 weeks)
    '2014-04-29'         # The 29th of April, 2014.
    '2014-04-29T15:00Z'  # 15:00 UTC on 29th of April, 2014.

Note that the strings returned  by `isoformat()` are not unique in the same way that the representational strings are.  For example, `'2014-04'` may represent either the quarter `2014-Q2` or the month `2014-04`.  Similarly, the isoformat string `'2014-04-29T15:00Z'` may represent either a complete hour span or a single minute span.

---

## Sequences of periods

The `periodical` module provides functions for returning sequences of time or date periods.  These allow you to easily return ranges such as "the last 24 hours", or "all the weeks since the start of the year".

### time_periods_ascending(time, span, num_periods)

### date_periods_ascending(date, span, num_periods)

Returns a list of `TimePeriod` or `DatePeriod` objects in chronological order, starting with a given time or date.

##### Arguments:

* `time`/`date` **(Optional)** - The starting time or date.  If not provided, this defaults to the current time or day.
* `span` - A string representing the period length.
* `num_periods` - An integer representing the number of `DatePeriod` objects to return.

Example result from `date_periods_ascending(span='monthly', num_periods=3)` on Nov 25th, 2014.

       Nov 25th 2014
           |
           V
    +--------+--------+--------+
    |  Nov.  |  Dec.  |  Jan.  |
    |  2014  |  2014  |  2015  |
    +--------+--------+--------+
       [0] ---> [1] ---> [2]

Example code:

    >>> periodical.date_periods_ascending(span='monthly', num_periods=3)
    [<DatePeriod '2014-11'>, <DatePeriod '2014-12'>, <DatePeriod '2015-01'>]

### time_periods_descending(time, span, num_periods)

### date_periods_descending(date, span, num_periods)

Returns a list of `TimePeriod` or `DatePeriod` objects in reverse chronological order, starting with a given time or date.

##### Arguments:

* `time`/`date` **(Optional)** - The starting time or date.  If not provided, this defaults to the current time or day.
* `span` - A string representing the period length.
* `num_periods` - An integer representing the number of `DatePeriod` objects to return.

Example result from `date_periods_descending(span='monthly', num_periods=3)` on Nov 25th, 2014.

                       Nov 25th 2014
                             |
                             V
    +--------+--------+--------+
    |  Sept. |  Oct.  |  Nov.  |
    |  2014  |  2014  |  2014  |
    +--------+--------+--------+
       [2] <--- [1] <--- [0]


Example code:

    >>> periodical.date_periods_descending(span='monthly', num_periods=3)
    [<DatePeriod '2014-11'>, <DatePeriod '2014-10'>, <DatePeriod '2014-09'>]

### time_periods_between(time_from, time_until, period)

### date_periods_between(date_from, date_until, period)

Returns a list of `TimePeriod` or `DatePeriod` objects in *either* chronological *or* reverse chronological order, starting and ending with a pair of given datetimes or dates.

##### Arguments:

* `time_from`/`date_from` **(Optional)** - The starting time or date.  If not provided, this defaults to the current time or day.
* `time_until`/`date_until` **(Optional)** - The ending time or date.  If not provided, this defaults to the current time or day.
* `span` - A string representing the period length.

Example result from `date_periods_between(date_until=datetime.date(2014, 12, 31), span='monthly')` on Sept 23rd, 2014.

    Sept 23rd 2014                 Dec 31st 2014
          |                             |
          V                             V
    +--------+--------+--------+--------+
    |  Sept. |  Oct.  |  Nov.  |  Dec.  | 
    |  2014  |  2014  |  2014  |  2014  |
    +--------+--------+--------+--------+
       [0] ---> [1] ---> [2] ---> [3]

Example code:

    >>> periodical.date_periods_between(date_until=datetime.date(2014, 12, 31), span='monthly')
    [<DatePeriod '2014-09'>, <DatePeriod '2014-10'>, <DatePeriod '2014-11'>, <DatePeriod '2014-12'>]

---

## Aggregation of values

For the following documentation we're going to need a set of data points that we're interested in aggregating, in order to demonstate how the different aggregation functions work.

We'll also need a set of periods that we're interested in aggregating the data against.

Our initial data looks like this:

    >>> start = date(2014, 09, 01)
    >>> periods = periodical.date_periods_ascending(start, num_periods = 4)
    >>> data_points = [
        (datetime.date(2014, 9, 1), 20),
        (datetime.date(2014, 9, 2), 25),
        (datetime.date(2014, 10, 1), 20),
        (datetime.date(2014, 10, 1), 20),
        (datetime.date(2014, 12, 1), 30)
    ]

### map(periods, data_points, transform=None)

Given a sequence of time periods and a set of events, maps each event into it's containing period.

* `periods`: A list of DatePeriod or TimePeriod instances.
* `times_value_pairs`: A list of two-tuples of the form `(date or datetime, value)`.
* `transform`: If provided, this should be a function that takes a single argument. The function will be applied to the list of values contained in each period in order to generate the output for that period.

Returns an ordered dictionary that maps each period to a list of the contained values.

     >>> periodical.map(periods, data_points)
     OrderedDict([
         (<DatePeriod '2014-09'>, [20, 25]),
         (<DatePeriod '2014-10'>, [20, 20]),
         (<DatePeriod '2014-11'>, []),
         (<DatePeriod '2014-12'>, [30])
     ])

### summation(periods, data_points, zero=0)

Given a sequence of time periods and a set of data points, produces the sum of data points within each period.

**Arguments**:

* `periods`: A list of DatePeriod or TimePeriod instances.
* `times_value_pairs`: A list of two-tuples of the form `(date or datetime, value)`.
* `zero`: The initial value to use for summations.  If using non-integer type you may wish to set this to ensure that zero values in the return result have the same type as non-zero values.  For example, you might set the zero argument to `0.0` or `Decimal('0')`. **(Optional)**

Returns an ordered dictionary that sums the values of the data points contained in each period.

     >>> periodical.summation(periods, data_points)
     OrderedDict([
         (<DatePeriod '2014-09'>, 45),
         (<DatePeriod '2014-10'>, 40),
         (<DatePeriod '2014-11'>, 0),
         (<DatePeriod '2014-12'>, 30)
     ])

### average(periods, data_points)

Given a sequence of time periods and a set of data points, produces the average of data points within each period.

**Arguments**:

* `periods`: A list of DatePeriod or TimePeriod instances.
* `times_value_pairs`: A list of two-tuples of the form `(date or datetime, value)`.

Returns an ordered dictionary that sums the values of the data points contained in each period.  Periods which do not contain any data points will be mapped to `None`.

     >>> periodical.average(periods, data_points)
     OrderedDict([
         (<DatePeriod '2014-09'>, 22.5),
         (<DatePeriod '2014-10'>, 20.0),
         (<DatePeriod '2014-11'>, None),
         (<DatePeriod '2014-12'>, 30.0)
     ])
 
### count(periods, times)

Counts the number of occurances of an event within each period.

**Arguments**:

* `periods`: A list of DatePeriod or TimePeriod instances.
* `times`: A list of date or datetime instances.

Returns an ordered dictionary that maps each period to the corresponding count of the number of date or time instances that it contained.

     >>> times = [date for (date, value) in data_points]
     >>> periodical.count(periods, times)
     OrderedDict([
         (<DatePeriod '2014-09'>, 2),
         (<DatePeriod '2014-10'>, 2),
         (<DatePeriod '2014-11'>, 0),
         (<DatePeriod '2014-12'>, 1)
     ])

## Timezone utilities

The periodical library includes a few utility classes to make it easier to work with properly timezone-aware datetime objects.

### UTC

A `tzinfo` class for representing the UTC timezone.

    >>> time = datetime.datetime(2014, 01, 01, tzinfo=periodical.UTC())
    >>> time
    datetime.datetime(2014, 1, 1, 0, 0, tzinfo=<UTC>)

### Offset

A `tzinfo` class for representing the timezone with the given offset.  The offset string must be specified in the form `+HH:MM` or `-HH:MM`.

    >>> time = datetime.datetime(2014, 01, 01, tzinfo=periodical.Offset('-05:00'))
    >>> time
    datetime.datetime(2014, 1, 1, 0, 0, tzinfo=<Offset '-05:00'>)

### utcnow()

Returns a `datetime` instance representing the current time in UTC, with an attached `UTC` timzone instance.

    >>> now = periodical.utcnow()
    >>> now
    datetime.datetime(2014, 1, 30, 13, 39, 13, 515377, tzinfo=<UTC>)

### utctoday()

Returns a `datetime` instance representing the current date within the UTC timezone.

    >>> today = periodical.utctoday()
    >>> today
    datetime.date(2014, 1, 30) 

### utc_datetime(\*args, \*\*kwargs)

Returns a new `datetime` instance representing the given time, with an attached `UTC` timzone instance.

    >>> time = periodical.utc_datetime(2014, 01, 01, 14, 30)
    >>> time
    datetime.datetime(2014, 1, 1, 14, 30, tzinfo=<UTC>)
