# Periodical

**A library for working with time and date series in Python.**

The `periodical` Python module provides a convienient way of dealing with time and date series.  

These are particular useful for aggregating events at differing time granualities, for example when generating graphs or reports covering a given time span.

You can install the `periodical` module using pip:

    pip install periodical

---

## Basic usage

### The TimePeriod and DatePeriod classes

The `TimePeriod` class is used to represent an interval of datetimes.

The `DatePeriod` class is used to represent an interval of dates.

You can instantiate a `TimePeriod` or `DatePeriod` object by specifying a time span.  For  `DatePeriod` this may be one of `'day'`, `'week'`, `'month'`, `'quarter'` or `'year'`.

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

#### Start and end dates

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

#### Differences between time and date periods

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


#### Iterating through periods

To return a new `TimePeriod` or `DatePeriod` object that occurs immediately before or after the existing period, you can call the `.next()` and `.previous()` methods.

    >>> period = periodical.DatePeriod(date=datetime.date(2014, 01, 05), span='week')
    >>> period.next()
    <DatePeriod '2014-W02'>
    >>> period.previous()
    <DatePeriod '2013-W52'>

#### String representations

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

## Working with sequences of periods

The `periodical` module provides functions for returning sequences of time or date periods.  These allow you to easily return ranges such as "the last 24 hours", or "all the weeks since the start of the year".

### time_periods_ascending(time, period, num_periods)

### date_periods_ascending(date, period, num_periods)

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

### time_periods_descending(time, period, num_periods)

### date_periods_descending(date, period, num_periods)

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

### map(periods, time_value_pairs, transform=None)

     {
         <DatePeriod '2014-09'>: [20, 25],
         <DatePeriod '2014-10'>: [20, 20],
         <DatePeriod '2014-11'>: [],
         <DatePeriod '2014-12'>: [30]
     }

### summation(periods, time_value_pairs)

     {
         <DatePeriod '2014-09'>: 45,
         <DatePeriod '2014-10'>: 40,
         <DatePeriod '2014-11'>: 0,
         <DatePeriod '2014-12'>: 30
     }

### average(periods, time_value_pairs)

     {
         <DatePeriod '2014-09'>: 22.5,
         <DatePeriod '2014-10'>: 20.0,
         <DatePeriod '2014-11'>: None,
         <DatePeriod '2014-12'>: 30.0
     }
 
### count(periods, times)

     {
         <DatePeriod '2014-09'>: 2,
         <DatePeriod '2014-10'>: 2,
         <DatePeriod '2014-11'>: 0,
         <DatePeriod '2014-12'>: 1
     }

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

    now = periodical.utcnow()
    datetime.datetime(2014, 1, 30, 13, 39, 13, 515377, tzinfo=<UTC>)

### utc_datetime(*args, **kwargs)

Returns a new `datetime` instance representing the given time, with an attached `UTC` timzone instance.

    time = periodical.utc_datetime(2014, 01, 01, 14, 30)
    datetime.datetime(2014, 1, 1, 14, 30, tzinfo=<UTC>)
