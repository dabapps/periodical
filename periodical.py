# coding: utf-8

import calendar
import collections
import datetime
import re

__version__ = '0.2'


yearly_re = re.compile('(?P<year>[0-9]+)$')
quarterly_re = re.compile('(?P<year>[0-9]+)[-/][Qq](?P<quarter>[0-9]+)$')
monthly_re = re.compile('(?P<year>[0-9]+)[-/](?P<month>[0-9]+)$')
weekly_re = re.compile('(?P<year>[0-9]+)[-/][Ww](?P<quarter>[0-9]+)$')
daily_re = re.compile('(?P<year>[0-9]+)[-/](?P<month>[0-9]+)[-/](?P<day>[0-9]+)$')
hour_re = re.compile('(?P<year>[0-9]+)[-/](?P<month>[0-9]+)[-/](?P<day>[0-9]+)[T ](?P<hour>[0-9]+)$')
minute_re = re.compile('(?P<year>[0-9]+)[-/](?P<month>[0-9]+)[-/](?P<day>[0-9]+)[T ](?P<hour>[0-9]+):(?P<minute>[0-9]+)$')
second_re = re.compile('(?P<year>[0-9]+)[-/](?P<month>[0-9]+)[-/](?P<day>[0-9]+)[T ](?P<hour>[0-9]+):(?P<minute>[0-9]+):(?P<second>[0-9]+)$')

timezone_re = re.compile('(?P<sign>[+-])(?P<hours>[0-9][0-9]):(?P<minutes>[0-9][0-9])')


class UTC(datetime.tzinfo):
    """
    UTC timezone class.
    """
    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return datetime.timedelta(0)


class Offset(datetime.tzinfo):
    """
    UTC timezone class.
    """
    def __init__(self, offset_repr):
        result = timezone_re.match(offset_repr)
        assert result, "Invalid timezone offset string, '%s'" % offset_repr
        sign, hours, minutes = result.groups()
        offset = datetime.timedelta(hours=int(hours), minutes=int(minutes))
        self._offset_repr = offset_repr
        self._offset = -offset if sign == '-' else offset

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return self._offset_repr

    def dst(self, dt):
        return self._offset


def utcnow():
    """
    As `datetime.datetime.utcnow()`, but returns a timezone aware datetime in UTC.
    """
    return datetime.datetime.utcnow().replace(tzinfo=UTC())


def utc_datetime(*args, **kwargs):
    """
    As `datetime.datetime()`, but returns a timezone aware datetime in UTC.
    """
    kwargs['tzinfo'] = UTC()
    return datetime.datetime(*args, **kwargs)


def _strip_hhmmss(time):
    return time.replace(hour=0, minute=0, second=0)


def _incr_month(month, amount=1):
    return ((month + amount) % 12) or 12


def _decr_month(month, amount=1):
    return ((month - amount) % 12) or 12


def _repr_to_date_and_span(string_repr):
    """
    Given a date period representation, return a two-tuple of the
    corresponding start date and string time span.

    eg. '2001-04' -> (date(2001, 04, 01), 'daily')
    """
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

    return (date, span)


def _repr_to_time_and_span(string_repr):
    """
    Given a time period representation, return a two-tuple of the
    corresponding start date and string time span.

    eg. '2001-04' -> (datetime(2001, 04, 01), 'daily')
    """
    if string_repr.endswith('Z'):
        tzinfo = UTC()
        string_repr = string_repr[:-1]
    elif string_repr.endswith('+00:00') or string_repr.endswith('-00:00'):
        tzinfo = UTC()
        string_repr = string_repr[:-6]
    elif timezone_re.match(string_repr[-6:]):
        tzinfo = Offset(string_repr[-6:])
        string_repr = string_repr[:-6]
    else:
        tzinfo = None

    yearly_result = yearly_re.match(string_repr)
    quarerly_result = quarterly_re.match(string_repr)
    monthly_result = monthly_re.match(string_repr)
    weekly_result = weekly_re.match(string_repr)
    daily_result = daily_re.match(string_repr)
    hour_result = hour_re.match(string_repr)
    minute_result = minute_re.match(string_repr)
    second_result = second_re.match(string_repr)

    if yearly_result:
        (year,) = yearly_result.groups()
        time = datetime.datetime(int(year), 1, 1)
        span = 'yearly'
    elif quarerly_result:
        (year, quarter) = quarerly_result.groups()
        time = datetime.datetime(int(year), (int(quarter) * 3) - 2, 1)
        span = 'quarterly'
    elif monthly_result:
        (year, month) = monthly_result.groups()
        time = datetime.datetime(int(year), int(month), 1)
        span = 'monthly'
    elif weekly_result:
        # ISO 8601 dates always include 4th Jan in the first week.
        # We populate a date that will be in the correct week period.
        (year, week) = weekly_result.groups()
        time = (
            datetime.datetime(int(year), 1, 4) +
            datetime.timedelta(days=(int(week) * 7) - 7)
        )
        span = 'weekly'
    elif daily_result:
        (year, month, day) = daily_result.groups()
        time = datetime.datetime(int(year), int(month), int(day))
        span = 'daily'
    elif hour_result:
        (year, month, day, hour) = hour_result.groups()
        time = datetime.datetime(int(year), int(month), int(day), int(hour))
        span = 'hour'
    elif minute_result:
        (year, month, day, hour, minute) = minute_result.groups()
        time = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
        span = 'minute'
    elif second_result:
        (year, month, day, hour, minute, second) = second_result.groups()
        time = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        span = 'second'
    else:
        raise ValueError('Unknown datetime representation')

    if tzinfo:
        time = time.replace(tzinfo=tzinfo)

    return (time, span)


class DatePeriod(object):
    """
    An immuntable object that represents a calendering period,
    which may be one of: daily, weekly, monthly, quarterly, yearly.
    """
    def __init__(self, string_repr=None, date=None, span=None, _start=None, _end=None, _today_func=None):
        self.today_func = datetime.date.today if _today_func is None else _today_func

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
            date, span = _repr_to_date_and_span(string_repr)

        # Create a DatePeriod by supplying a date and span.
        assert span is not None, '`span` argument not supplied.'

        if date is None:
            date = self.today_func()

        try:
            self._span = {
                'day': 'daily',
                'dai': 'daily',
                'wee': 'weekly',
                'mon': 'monthly',
                'qua': 'quarterly',
                'yea': 'yearly'
            }[span.lower()[:3]]
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
        if self.span == 'daily':
            start = self.start - datetime.timedelta(days=1)
            end = self.end - datetime.timedelta(days=1)
        elif self.span == 'weekly':
            start = self.start - datetime.timedelta(days=7)
            end = self.end - datetime.timedelta(days=7)
        elif self.span == 'monthly':
            year = self.start.year - 1 if self.start.month == 1 else self.start.year
            start_month = _decr_month(self.start.month)
            end_month = _decr_month(self.end.month)
            end_day = calendar.monthrange(year, end_month)[1]
            start = self.start.replace(month=start_month, year=year)
            end = self.end.replace(day=end_day, month=end_month, year=year)
        elif self._span == 'quarterly':
            year = self._start.year
            if self._start.month == 1:
                year -= 1
            start_month = _decr_month(self.start.month, 3)
            end_month = _decr_month(self.end.month, 3)
            end_day = calendar.monthrange(year, end_month)[1]
            start = self.start.replace(month=start_month, year=year)
            end = self.end.replace(day=end_day, month=end_month, year=year)
        else:  # self._span == 'yearly'
            year = self.start.year - 1
            start = self.start.replace(year)
            end = self.end.replace(year)

        return DatePeriod(span=self.span, _start=start, _end=end)

    def next(self):
        """
        Return a new DatePeriod representing the period
        immediately following this one.
        """
        if self.span == 'daily':
            start = self.start + datetime.timedelta(days=1)
            end = self.end + datetime.timedelta(days=1)
        elif self.span == 'weekly':
            start = self.start + datetime.timedelta(days=7)
            end = self.end + datetime.timedelta(days=7)
        elif self.span == 'monthly':
            year = self.start.year + 1 if self.start.month == 12 else self.start.year
            start_month = _incr_month(self.start.month)
            end_month = _incr_month(self.end.month)
            end_day = calendar.monthrange(year, end_month)[1]
            start = self.start.replace(month=start_month, year=year)
            end = self.end.replace(day=end_day, month=end_month, year=year)
        elif self._span == 'quarterly':
            year = self.start.year + 1 if self.start.month >= 10 else self.start.year
            start_month = _incr_month(self.start.month, 3)
            end_month = _incr_month(self.end.month, 3)
            end_day = calendar.monthrange(year, end_month)[1]
            start = self.start.replace(month=start_month, year=year)
            end = self.end.replace(day=end_day, month=end_month, year=year)
        else:  # self._span == 'yearly'
            year = self.start.year + 1
            start = self.start.replace(year)
            end = self.end.replace(year)

        return DatePeriod(span=self.span, _start=start, _end=end)

    def isoformat(self):
        """
        Return an ISO8601 formatted string representing the period.
        """
        if self.span == 'daily':
            # YYYY-MM-DD
            return self.start.isoformat()
        elif self.span == 'weekly':
            # YYYY-W##
            iso_year, iso_week, iso_day = self.start.isocalendar()
            return '%d-W%02d' % (iso_year, iso_week)
        elif self.span in ('monthly', 'quarterly'):
            # YYYY-MM
            return self.start.isoformat()[:7]
        else:
            # YYYY
            return str(self.start.year)

    def contains(self, date):
        """
        Returns `True` if the given date is contained by this period.
        """
        return date >= self.start and date <= self.end

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
            return "%04d-Q%01d" % (self.start.year, (self.end.month / 3))
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
        return self.start > other.end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end


class TimePeriod(object):
    """
    An immuntable object that represents a calendering period,
    which may be one of: daily, weekly, monthly, quarterly, yearly.
    """
    def __init__(self, string_repr=None, time=None, span=None, _start=None, _end=None, _now_func=None):
        self.now_func = utcnow if _now_func is None else _now_func

        if _start is not None and _end is not None:
            # Created a new DatePeriod with explicit start and end dates,
            # as a result of calling `.previous()` or `.next()`.
            self._span = span
            self._start = _start
            self._end = _end
            return

        if string_repr:
            # Create a DatePeriod by supplying a string representation.
            assert time is None, 'Cannot supply both `string_repr` and `time`'
            assert span is None, 'Cannot supply both `string_repr` and `span`'
            time, span = _repr_to_time_and_span(string_repr)

        # Create a DatePeriod by supplying a date and span.
        assert span is not None, '`span` argument not supplied.'

        if time is None:
            time = self.now_func()

        try:
            self._span = {
                'sec': 'seconds',
                'min': 'minutes',
                'hou': 'hours',
                'day': 'daily',
                'dai': 'daily',
                'wee': 'weekly',
                'mon': 'monthly',
                'qua': 'quarterly',
                'yea': 'yearly'
            }[span.lower()[:3]]
        except KeyError:
            raise ValueError("Invalid value for `span` argument '%s'" % span)

        if self._span == 'seconds':
            self._start = time
            self._end = time + datetime.timedelta(seconds=1)
        elif self._span == 'minutes':
            self._start = time.replace(second=0)
            self._end = time.replace(second=0) + datetime.timedelta(minutes=1)
        elif self._span == 'hours':
            self._start = time.replace(minute=0, second=0)
            self._end = time.replace(minute=0, second=0) + datetime.timedelta(hours=1)
        elif self._span == 'daily':
            self._start = _strip_hhmmss(time)
            self._end = _strip_hhmmss(time) + datetime.timedelta(days=1)
        elif self._span == 'weekly':
            weekday = time.weekday()  # 0..6
            self._start = _strip_hhmmss(time) - datetime.timedelta(days=weekday)
            self._end = _strip_hhmmss(time) + datetime.timedelta(days=(7 - weekday))
        elif self._span == 'monthly':
            en_month = _incr_month(time.month)
            en_year = time.year + 1 if time.month == 12 else time.year
            self._start = _strip_hhmmss(time).replace(day=1)
            self._end = _strip_hhmmss(time).replace(year=en_year, month=en_month, day=1)
        elif self._span == 'quarterly':
            current_quarter = int((time.month - 1) / 3)  # In the range 0..3
            st_month = (current_quarter * 3) + 1               # (1, 4, 7, 10)
            en_month = _incr_month((current_quarter * 3), 4)   # (4, 7, 10, 1)
            en_year = time.year + 1 if current_quarter == 3 else time.year
            self._start = _strip_hhmmss(time).replace(month=st_month, day=1)
            self._end = _strip_hhmmss(time).replace(year=en_year, month=en_month, day=1)
        else:  # self._span == 'yearly':
            self._start = _strip_hhmmss(time).replace(month=1, day=1)
            self._end = _strip_hhmmss(time).replace(year=time.year + 1, month=1, day=1)

    def previous(self):
        """
        Return a new TimePeriod representing the period
        immediately prior to this one.
        """
        if self.span == 'seconds':
            start = self.start - datetime.timedelta(seconds=1)
            end = self.end - datetime.timedelta(seconds=1)
        elif self.span == 'minutes':
            start = self.start - datetime.timedelta(minutes=1)
            end = self.end - datetime.timedelta(minutes=1)
        elif self.span == 'hours':
            start = self.start - datetime.timedelta(hours=1)
            end = self.end - datetime.timedelta(hours=1)
        elif self.span == 'daily':
            start = self.start - datetime.timedelta(days=1)
            end = self.end - datetime.timedelta(days=1)
        elif self.span == 'weekly':
            start = self.start - datetime.timedelta(days=7)
            end = self.end - datetime.timedelta(days=7)
        elif self.span == 'monthly':
            start_year = self.start.year - 1 if self.start.month == 1 else self.start.year
            end_year = self.end.year - 1 if self.end.month == 1 else self.end.year
            start_month = _decr_month(self.start.month)
            end_month = _decr_month(self.end.month)
            start = self._start.replace(month=start_month, year=start_year)
            end = self._end.replace(month=end_month, year=end_year)
        elif self.span == 'quarterly':
            start_year = self.start.year - 1 if self.start.month == 1 else self.start.year
            end_year = self.end.year - 1 if self.end.month == 1 else self.end.year
            start_month = _decr_month(self.start.month, 3)
            end_month = _decr_month(self.end.month, 3)
            start = self._start.replace(month=start_month, year=start_year)
            end = self._end.replace(month=end_month, year=end_year)
        else:  # self._span == 'yearly'
            start = self.start.replace(self.start.year - 1)
            end = self.end.replace(self.end.year - 1)

        return TimePeriod(span=self.span, _start=start, _end=end)

    def next(self):
        """
        Return a new TimePeriod representing the period
        immediately following this one.
        """
        if self._span == 'seconds':
            start = self.start + datetime.timedelta(seconds=1)
            end = self.end + datetime.timedelta(seconds=1)
        elif self._span == 'minutes':
            start = self.start + datetime.timedelta(minutes=1)
            end = self.end + datetime.timedelta(minutes=1)
        elif self._span == 'hours':
            start = self.start + datetime.timedelta(hours=1)
            end = self.end + datetime.timedelta(hours=1)
        elif self._span == 'daily':
            start = self.start + datetime.timedelta(days=1)
            end = self.end + datetime.timedelta(days=1)
        elif self._span == 'weekly':
            start = self.start + datetime.timedelta(days=7)
            end = self.end + datetime.timedelta(days=7)
        elif self._span == 'monthly':
            start_year = self.start.year + 1 if self.start.month == 12 else self.start.year
            end_year = self.end.year + 1 if self.end.month == 12 else self.end.year
            start_month = _incr_month(self.start.month)
            end_month = _incr_month(self.end.month)
            start = self.start.replace(year=start_year, month=start_month)
            end = self.end.replace(year=end_year, month=end_month)
        elif self._span == 'quarterly':
            start_year = self.start.year + 1 if self.start.month >= 10 else self.start.year
            end_year = self.end.year + 1 if self.end.month >= 10 else self.end.year
            start_month = _incr_month(self._start.month, 3)
            end_month = _incr_month(self._end.month, 3)
            start = self.start.replace(year=start_year, month=start_month)
            end = self.end.replace(year=end_year, month=end_month)
        else:  # self._span == 'yearly'
            start = self.start.replace(self.start.year + 1)
            end = self.end.replace(self.end.year + 1)

        return TimePeriod(span=self.span, _start=start, _end=end)

    def isoformat(self):
        """
        Return an ISO8601 formatted string representing the period.
        """
        if self.span == 'seconds':
            # YYYY-MM-DDTHH:MM:SS
            ret = self.start.isoformat()[:19]
        elif self.span == 'minutes':
            # YYYY-MM-DDTHH:MM
            ret = self.start.isoformat()[:16]
        elif self.span == 'hours':
            # YYYY-MM-DDTHH
            ret = self.start.isoformat()[:13]
        elif self.span == 'daily':
            # YYYY-MM-DD
            ret = self.start.isoformat()[:10]
        elif self.span == 'weekly':
            # YYYY-W##
            iso_year, iso_week, iso_day = self.start.isocalendar()
            ret = '%d-W%02d' % (iso_year, iso_week)
        elif self.span in ('monthly', 'quarterly'):
            # YYYY-MM
            ret = self.start.isoformat()[:7]
        else:
            # YYYY
            ret = str(self.start.year)

        if self.start.tzinfo is not None:
            if self.start.utcoffset().seconds:
                ret += self.start.isoformat()[-6:]
            else:
                ret += 'Z'

        return ret

    def contains(self, time):
        """
        Returns `True` if the given datetime is contained by this period.
        """
        return time >= self.start and time < self.end

    def __repr__(self):
        """
        Returns a representation that uniquely identifies the time period.
        """
        return "<%s '%s'>" % (self.__class__.__name__, self)

    def __str__(self):
        """
        Returns a string that uniquely identifies the time period.
        """
        if self.span == 'quarterly':
            return "%04d-Q%01d" % (self.start.year, (self.end.month / 3))
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
        return self.start >= other.end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end


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


def time_periods_descending(time=None, span=None, num_periods=None):
    """
    Returns a list of TimePeriod instances, starting with a period that
    covers the given time and iterating through the preceeding periods.
    """
    assert num_periods is not None, '`num_periods` argument not supplied.'

    ret = []
    period = TimePeriod(time=time, span=span)
    for idx in range(num_periods):
        ret.append(period)
        period = period.previous()
    return ret


def time_periods_ascending(time=None, span=None, num_periods=None):
    """
    Returns a list of TimePeriod instances, starting with a period that
    covers the given time and iterating through the following periods.
    """
    assert num_periods is not None, '`num_periods` argument not supplied.'

    ret = []
    period = TimePeriod(time=time, span=span)
    for idx in range(num_periods):
        ret.append(period)
        period = period.next()
    return ret


def time_periods_between(time_from=None, time_until=None, span=None):
    """
    Returns a list of TimePeriod instances, starting and ending with
    periods that cover the given start and end times.
    """
    period = TimePeriod(time=time_from, span=span)
    until = TimePeriod(time=time_until, span=span)
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
