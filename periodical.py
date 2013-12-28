# coding: utf-8

import calendar
import collections
import datetime
import re

__version__ = '0.1'


yearly_re = re.compile('(?P<year>[0-9]+)$')
quarterly_re = re.compile('(?P<year>[0-9]+)[-/][Qq](?P<quarter>[0-9]+)$')
monthly_re = re.compile('(?P<year>[0-9]+)[-/](?P<month>[0-9]+)$')
weekly_re = re.compile('(?P<year>[0-9]+)[-/][Ww](?P<quarter>[0-9]+)$')
daily_re = re.compile('(?P<year>[0-9]+)[-/](?P<month>[0-9]+)[-/](?P<day>[0-9]+)$')


class DatePeriod(object):
    """
    An immuntable object that represents a calendering period,
    which may be one of: daily, weekly, monthly, quarterly, yearly.
    """
    today_func = datetime.date.today

    def __init__(self, string_repr=None, date=None, span=None, _start=None, _end=None):

        if _start is not None and _end is not None:
            # Created a new DatePeriod with explicit start and end dates,
            # as a result of calling `.previous()` or `.next()`.
            self._span = span
            self._start = _start
            self._end = _end
            return

        if string_repr:
            # Create a DatePeriod by supplying a string representation.
            assert date is None, 'Cannot supply both `string_repr` and `date`'
            assert span is None, 'Cannot supply both `string_repr` and `span`'

            yearly_result = yearly_re.match(string_repr)
            quarerly_result = quarterly_re.match(string_repr)
            monthly_result = monthly_re.match(string_repr)
            weekly_result = weekly_re.match(string_repr)
            daily_result = daily_re.match(string_repr)

            if yearly_result:
                (year,) = yearly_result.groups()
                date = datetime.date(int(year), 1, 1)
                span = 'yearly'
            elif quarerly_result:
                (year, quarter) = quarerly_result.groups()
                date = datetime.date(int(year), (int(quarter) * 3) - 2, 1)
                span = 'quarterly'
            elif monthly_result:
                (year, month) = monthly_result.groups()
                date = datetime.date(int(year), int(month), 1)
                span = 'monthly'
            elif weekly_result:
                # ISO 8601 dates always include 4th Jan in the first week.
                # We populate a date that will be in the correct week period.
                (year, week) = weekly_result.groups()
                date = (
                    datetime.date(int(year), 1, 4) +
                    datetime.timedelta(days=(int(week) * 7) - 7)
                )
                span = 'weekly'
            elif daily_result:
                (year, month, day) = daily_result.groups()
                date = datetime.date(int(year), int(month), int(day))
                span = 'daily'
            else:
                raise ValueError('Unknown date representation')

        # Create a DatePeriod by supplying a date and span.
        assert span is not None, '`span` argument not supplied.'

        if date is None:
            date = self.today_func()

        try:
            self._span = {
                'd': 'daily',
                'w': 'weekly',
                'm': 'monthly',
                'q': 'quarterly',
                'y': 'yearly'
            }[span.lower()[0]]
        except KeyError:
            raise ValueError("Invalid value for `span` argument '%s'" % span)

        if self._span == 'daily':
            self._start = date
            self._end = date
        elif self._span == 'weekly':
            weekday = date.weekday()  # 0..6
            self._start = date - datetime.timedelta(days=weekday)
            self._end = date + datetime.timedelta(days=(6 - weekday))
        elif self._span == 'monthly':
            month_end_day = calendar.monthrange(date.year, date.month)[1]
            self._start = datetime.date(date.year, date.month, 1)
            self._end = datetime.date(date.year, date.month, month_end_day)
        elif self._span == 'quarterly':
            current_quarter = int((date.month - 1) / 3)  # In the range 0..3
            st_month = (current_quarter * 3) + 1   # (1, 4, 7, 10)
            en_month = (current_quarter * 3) + 3   # (3, 6, 9, 12)
            month_end_day = calendar.monthrange(date.year, en_month)[1]
            self._start = datetime.date(date.year, st_month, 1)
            self._end = datetime.date(date.year, en_month, month_end_day)
        else:  # self._span == 'yearly':
            self._start = datetime.date(date.year, 1, 1)
            self._end = datetime.date(date.year, 12, 31)

    def previous(self):
        """
        Return a new DatePeriod representing the period
        immediately prior to this one.
        """
        if self._span == 'daily':
            start = self._start - datetime.timedelta(days=1)
            end = self._end - datetime.timedelta(days=1)
        elif self._span == 'weekly':
            start = self._start - datetime.timedelta(days=7)
            end = self._end - datetime.timedelta(days=7)
        elif self._span == 'monthly':
            year = self._start.year
            if self._start.month == 1:
                year -= 1
            start_month = ((self._start.month - 1) % 12) or 12
            end_month = ((self._end.month - 1) % 12) or 12
            end_day = calendar.monthrange(year, end_month)[1]
            start = self._start.replace(month=start_month, year=year)
            end = self._end.replace(day=end_day, month=end_month, year=year)
        elif self._span == 'quarterly':
            year = self._start.year
            if self._start.month == 1:
                year -= 1
            start_month = ((self._start.month - 3) % 12) or 12
            end_month = ((self._end.month - 3) % 12) or 12
            end_day = calendar.monthrange(year, end_month)[1]
            start = self._start.replace(month=start_month, year=year)
            end = self._end.replace(day=end_day, month=end_month, year=year)
        else:  # self._span == 'yearly'
            year = self._start.year - 1
            start = self._start.replace(year)
            end = self._end.replace(year)

        return DatePeriod(span=self.span, _start=start, _end=end)

    def next(self):
        """
        Return a new DatePeriod representing the period
        immediately following this one.
        """
        if self._span == 'daily':
            start = self._start + datetime.timedelta(days=1)
            end = self._end + datetime.timedelta(days=1)
        elif self._span == 'weekly':
            start = self._start + datetime.timedelta(days=7)
            end = self._end + datetime.timedelta(days=7)
        elif self._span == 'monthly':
            year = self._start.year
            if self._start.month == 12:
                year += 1
            start_month = ((self._start.month + 1) % 12) or 12
            end_month = ((self._end.month + 1) % 12) or 12
            end_day = calendar.monthrange(year, end_month)[1]
            start = self._start.replace(month=start_month, year=year)
            end = self._end.replace(day=end_day, month=end_month, year=year)
        elif self._span == 'quarterly':
            year = self._start.year
            if self._start.month == 10:
                year += 1
            start_month = ((self._start.month + 3) % 12) or 12
            end_month = ((self._end.month + 3) % 12) or 12
            end_day = calendar.monthrange(year, end_month)[1]
            start = self._start.replace(month=start_month, year=year)
            end = self._end.replace(day=end_day, month=end_month, year=year)
        else:  # self._span == 'yearly'
            year = self._start.year + 1
            start = self._start.replace(year)
            end = self._end.replace(year)

        return DatePeriod(span=self.span, _start=start, _end=end)

    def isoformat(self):
        """
        Return an ISO8601 formatted string representing the period.
        """
        if self.span == 'daily':
            # YYYY-MM-DD
            return self._start.isoformat()
        elif self.span == 'weekly':
            # YYYY-W##
            iso_year, iso_week, iso_day = self._start.isocalendar()
            return '%d-W%02d' % (iso_year, iso_week)
        elif self.span in ('monthly', 'quarterly'):
            # YYYY-MM
            return self._start.isoformat()[:7]
        else:
            # YYYY
            return str(self._start.year)

    def contains(self, date):
        """
        Returns `True` if the given date is contained by this period.
        """
        return date >= self._start and date <= self._end

    def __repr__(self):
        """
        Returns a representation that uniquely identifies the date period.
        """
        return "<%s '%s'>" % (self.__class__.__name__, self)

    def __str__(self):
        """
        Returns a representation that uniquely identifies the date period.
        """
        if self.span == 'quarterly':
            return "%04d-Q%01d" % (self._start.year, (self._end.month / 3))
        return self.isoformat()

    def __hash__(self):
        return hash(str(self))

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def span(self):
        return self._span

    def __gt__(self, other):
        return self._start > other._end

    def __eq__(self, other):
        return self._start == other._start and self._end == other._end


# Series functions

def date_periods_descending(date=None, span=None, num_periods=None):
    """
    Returns a list of DatePeriod instances, starting with a period that
    covers the given date and iterating through the preceeding periods.
    """
    assert num_periods is not None, '`num_periods` argument not supplied.'

    ret = []
    period = DatePeriod(date=date, span=span)
    for idx in range(num_periods):
        ret.append(period)
        period = period.previous()
    return ret


def date_periods_ascending(date=None, span=None, num_periods=None):
    """
    Returns a list of DatePeriod instances, starting with a period that
    covers the given date and iterating through the following periods.
    """
    assert num_periods is not None, '`num_periods` argument not supplied.'

    ret = []
    period = DatePeriod(date=date, span=span)
    for idx in range(num_periods):
        ret.append(period)
        period = period.next()
    return ret


def date_periods_between(date_from=None, date_until=None, span=None):
    """
    Returns a list of DatePeriod instances, starting and ending with
    periods that cover the given start and end dates.
    """
    period = DatePeriod(date=date_from, span=span)
    until = DatePeriod(date=date_until, span=span)
    ascending = until > period

    ret = []
    while not period == until:
        ret.append(period)
        period = period.next() if ascending else period.previous()
    ret.append(period)
    return ret


# Aggregation functions

def _next_pair_or_none(iterator):
    """
    Returns the next pair in an iterator of pairs, or a pair of None.
    """
    try:
        return next(iterator)
    except StopIteration:
        return (None, None)


def map(periods, date_value_pairs, transform=None):
    """
    Given a sequence of dates periods, and a list of date/value pairs,
    map each value to the period containing it's date.
    """
    is_descending = periods and (periods[0] > periods[-1])
    sort_by_date = lambda date_value_pair: date_value_pair[0]
    date_value_iter = iter(sorted(date_value_pairs, key=sort_by_date, reverse=is_descending))

    ret = collections.OrderedDict()
    date, value = _next_pair_or_none(date_value_iter)
    for period in periods:
        this_mapping = []
        while date is not None and period.contains(date):
            this_mapping.append(value)
            date, value = _next_pair_or_none(date_value_iter)

        if transform is not None:
            this_mapping = transform(this_mapping)

        ret[period] = this_mapping

    return ret


def summation(periods, date_value_pairs):
    return map(periods, date_value_pairs, transform=sum)


def average(periods, date_value_pairs):
    avg = lambda values: float(sum(values)) / len(values) if values else None
    return map(periods, date_value_pairs, transform=avg)


def count(periods, dates):
    date_value_pairs = [(date, None) for date in dates]
    return map(periods, date_value_pairs, transform=len)
