# Periodical

The `periodical` Python module provides a convienient way of dealing with daily, weekly, monthly, quarterly and yearly date intervals.

These are particular useful for aggregating events at differing time granualities, for example when generating graphs or reports covering a given time span.

You can install the `periodical` module using pip:

    pip install periodical

---

## Basic usage

### The DatePeriod class

The `DatePeriod` class is used to represent an interval of dates.

You can instantiate a `DatePeriod` object by specifying a date span as one of `'daily'`, `'weekly'`, `'monthly'`, `'quarterly'` or `'yearly'`.  The date period covering the current day will be returned.

    >>> period = periodical.DatePeriod(span='weekly')
    >>> period
    <DatePeriod '2013-W51'>

You can also explicitly provide a date that you wish the date period to cover.

	>>> date = datetime.date(2015, 1, 25)
    >>> period = periodical.DatePeriod(date=date, span='weekly')
    >>> period
    <DatePeriod '2015-W04'>

#### Start and end dates

A `DatePeriod` object provides `start` and `end` properties that return date objects.

    >>> period.start
    datetime.date(2013, 12, 16)

    >>> period.end
    datetime.date(2013, 12, 22)

The `DatePeriod` class also provide a `contains()` method that takes a date object and returns `True` if the date is contained by the given date period.

    >>> period.contains(datetime.date(2013, 12, 20))
    True

    >>> period.contains(datetime.date(2013, 12, 23))
    False

#### Iterating through date periods

To return a new `DatePeriod` object that occurs immediately before or after the existing period, you can call the `.next()` and `.previous()` methods.

    >>> period.next()
    <DatePeriod '2013-W52'>

    >>> period.previous()
    <DatePeriod '2013-W50'>

#### String representations

DatePeriod objects use a unique representation that follows ISO 8601, with the exception of quarterley intervals, which use a 'Q' prefix to the quarter. 

The following are all valid representations of DatePeriod objects:

    <DatePeriod '2015'>        # The 2015 year.
    <DatePeriod '2013-Q2'>     # The second quarter of 2013.
    <DatePeriod '2014-03'>     # March, 2014.
    <DatePeriod '2013-W24'>    # The 24th week of 2013.  (Numbering by ISO 8601 weeks)
    <DatePeriod '2014-04-29'>  # The 29th of April, 2014.

You can also instantiate a `DatePeriod` object using it's unique representation.

    >>> period = periodical.DatePeriod("2014-Q1")
    >>> period.start
    datetime.date(2014, 1, 1)
    >>> period.end
    datetime.date(2014, 3, 31)

The `isoformat()` method returns an ISO 8601 formatted date representing the start of the date range.  Note that quarterly representations cannot be expressed in ISO 8601, so will simply return the monthly representation of the start date.

    '2015'        # The 2015 year.
    '2013-04'     # The second quarter of 2013.
    '2014-03'     # March, 2014.
    '2013-W24'    # The 24th week of 2013.  (Numbering by ISO 8601 weeks)
    '2014-04-29'  # The 29th of April, 2014.

---

## Working with sequences of date periods

The `periodical` module provides a few functions for returning sequences of date periods.  These allow you to easily return ranges such as "the last 12 months", or "all the weeks since the start of the year".

### periods_ascending(from, period, num_periods)

Returns a list of `DatePeriod` objects in chronological order, starting with a given date.

##### Arguments:

* `from` **(Optional)** - The starting date.  If not provided, this defaults to the current day.
* `span` - A string representing the period length.
* `num_periods` - An integer representing the number of `DatePeriod` objects to return.

Example result from `periods_ascending(span='monthly', num_periods=3)` on Nov 25th, 2014.

       Nov 25th 2014
           |
           V
    +--------+--------+--------+
    |  Nov.  |  Dec.  |  Jan.  |
    |  2014  |  2014  |  2015  |
    +--------+--------+--------+
       [0] ---> [1] ---> [2]

Example code:

    >>> periodical.periods_ascending(span='monthly', num_periods=3)
    [<DatePeriod '2014-11'>, <DatePeriod '2014-12'>, <DatePeriod '2015-01'>]

### periods_descending(from, period, num_periods)

Returns a list of `DatePeriod` objects in reverse chronological order, starting with a given date.

##### Arguments:

* `from` **(Optional)** - The starting date.  If not provided, this defaults to the current day.
* `span` - A string representing the period length.
* `num_periods` - An integer representing the number of `DatePeriod` objects to return.

Example result from `periods_descending(span='monthly', num_periods=3)` on Nov 25th, 2014.

                       Nov 25th 2014
                             |
                             V
    +--------+--------+--------+
    |  Sept. |  Oct.  |  Nov.  |
    |  2014  |  2014  |  2014  |
    +--------+--------+--------+
       [2] <--- [1] <--- [0]


Example code:

    >>> periodical.periods_descending(span='monthly', num_periods=3)
    [<DatePeriod '2014-11'>, <DatePeriod '2014-10'>, <DatePeriod '2014-09'>]

### periods_between(date_from, date_until, period)

Returns a list of `DatePeriod` objects in *either* chronological *or* reverse chronological order, starting and ending with a pair of given dates.

##### Arguments:

* `date_from` **(Optional)** - The starting date.  If not provided, this defaults to the current day.
* `date_until` **(Optional)** - The ending date.  If not provided, this defaults to the current day.
* `span` - A string representing the period length.

Example result from `periods_between(date_until=datetime.date(2014, 12, 31), span='monthly')` on Sept 23rd, 2014.

    Sept 23rd 2014                 Dec 31st 2014
          |                             |
          V                             V
    +--------+--------+--------+--------+
    |  Sept. |  Oct.  |  Nov.  |  Dec.  | 
    |  2014  |  2014  |  2014  |  2014  |
    +--------+--------+--------+--------+
       [0] ---> [1] ---> [2] ---> [3]

Example code:

    >>> periodical.periods_between(date_until=datetime.date(2014, 12, 31), span='monthly')
    [<DatePeriod '2014-09'>, <DatePeriod '2014-10'>, <DatePeriod '2014-11'>, <DatePeriod '2014-12'>]

---

## Aggregation of values

### map(periods, date_value_pairs, transform=None)

     {
         <DatePeriod '2014-09'>: [20, 25],
         <DatePeriod '2014-10'>: [20, 20],
         <DatePeriod '2014-11'>: [],
         <DatePeriod '2014-12'>: [30]
     }

### summation(periods, date_value_pairs)

     {
         <DatePeriod '2014-09'>: 45,
         <DatePeriod '2014-10'>: 40,
         <DatePeriod '2014-11'>: 0,
         <DatePeriod '2014-12'>: 30
     }

### average(periods, date_value_pairs)

     {
         <DatePeriod '2014-09'>: 22.5,
         <DatePeriod '2014-10'>: 20.0,
         <DatePeriod '2014-11'>: None,
         <DatePeriod '2014-12'>: 30.0
     }
 
### count(periods, dates)

     {
         <DatePeriod '2014-09'>: 2,
         <DatePeriod '2014-10'>: 2,
         <DatePeriod '2014-11'>: 0,
         <DatePeriod '2014-12'>: 1
     }
