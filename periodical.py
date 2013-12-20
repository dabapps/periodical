# coding: utf-8

import calendar
import datetime

__version__ = '0.1'


class CalendarPeriod(object):
    """
    An immuntable object that represents a calendering period,
    which may be one of: daily, weekly, monthly, quarterly, yearly.
    """
    today_func = datetime.date.today

    def __init__(self, date=None, period='daily', start=None, end=None):
        if start is not None and end is not None:
            # Explictly created new CalendarPeriod by calling `.previous()`.
            self._period = period
            self._start = start
            self._end = end
            return

        # Created a CalendarPeriod by supplying a date and period.
        if date is None:
            date = self.today_func()

        try:
            self._period = {
                'd': 'daily',
                'w': 'weekly',
                'm': 'monthly',
                'q': 'quarterly',
                'y': 'yearly'
            }[period.lower()[0]]
        except KeyError:
            raise ValueError("Invalid period '%s'" % period)

        if self._period == 'daily':
            self._start = date
            self._end = date
        elif self._period == 'weekly':
            weekday = date.weekday()  # 0..6
            self._start = date - datetime.timedelta(days=weekday)
            self._end = date + datetime.timedelta(days=(6 - weekday))
        elif self._period == 'monthly':
            month_end_day = calendar.monthrange(date.year, date.month)[1]
            self._start = datetime.date(date.year, date.month, 1)
            self._end = datetime.date(date.year, date.month, month_end_day)
        elif self._period == 'quarterly':
            current_quarter = int((date.month - 1) / 3)  # In the range 0..3
            st_month = (current_quarter * 3) + 1   # (1, 4, 7, 10)
            en_month = (current_quarter * 3) + 3   # (3, 6, 9, 12)
            month_end_day = calendar.monthrange(date.year, en_month)[1]
            self._start = datetime.date(date.year, st_month, 1)
            self._end = datetime.date(date.year, en_month, month_end_day)
        else:  # self._period == 'yearly':
            self._start = datetime.date(date.year, 1, 1)
            self._end = datetime.date(date.year, 12, 31)

    def previous(self):
        """
        Return a new CalendarPeriod representing the period
        immediately prior to this one.
        """
        if self._period == 'daily':
            start = self._start - datetime.timedelta(days=1)
            end = self._end - datetime.timedelta(days=1)
        elif self._period == 'weekly':
            start = self._start - datetime.timedelta(days=7)
            end = self._end - datetime.timedelta(days=7)
        elif self._period == 'monthly':
            year = self._start.year
            if self._start.month == 1:
                year -= 1
            start_month = ((self._start.month - 1) % 12) or 12
            end_month = ((self._end.month - 1) % 12) or 12
            end_day = calendar.monthrange(year, end_month)[1]
            start = self._start.replace(month=start_month, year=year)
            end = self._end.replace(day=end_day, month=end_month, year=year)
        elif self._period == 'quarterly':
            year = self._start.year
            if self._start.month == 1:
                year -= 1
            start_month = ((self._start.month - 3) % 12) or 12
            end_month = ((self._end.month - 3) % 12) or 12
            end_day = calendar.monthrange(year, end_month)[1]
            start = self._start.replace(month=start_month, year=year)
            end = self._end.replace(day=end_day, month=end_month, year=year)
        else:  # self._period == 'yearly'
            year = self._start.year - 1
            start = self._start.replace(year)
            end = self._end.replace(year)

        return CalendarPeriod(period=self.period, start=start, end=end)

    def isoformat(self):
        """
        Return an ISO8601 formatted string representing the period.
        """
        if self.period == 'daily':
            # YYYY-MM-DD
            return self._start.isoformat()
        elif self.period == 'weekly':
            # YYYY-W##
            iso_year, iso_week, iso_day = self._start.isocalendar()
            return '%d-W%02d' % (iso_year, iso_week)
        elif self.period in ('monthly', 'quarterly'):
            # YYYY-MM
            return self._start.isoformat()[:7]
        else:
            # YYYY
            assert self.period == 'yearly', 'self.period had invalid value'
            return str(self._start.year)

    def contains(self, date):
        """
        Returns `True` if the given date is contained by this period.
        """
        return date >= self._start and date <= self._end

    def __repr__(self):
        """
        Returns a representation that uniquely identifies the calendar period.
        """
        if self.period == 'quarterly':
            date_repr = "%04d-Q%d" % (self._start.year, (self._end.month / 3))
        else:
            date_repr = self.isoformat()
        return "<%s '%s'>" % (self.__class__.__name__, date_repr)

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def period(self):
        return self._period


def get_periods_descending(date=None, period='daily', num_periods=None):
    """
    Returns a list of CalendarPeriod instances, starting with a period that
    covers the given date and iterating through the preceeding periods.
    """
    cal = CalendarPeriod(date, period)

    if num_periods is None:
        num_periods = {
            'd': 365,
            'w': 52,
            'm': 12,
            'q': 4,
            'y': 1
        }[period.lower()[0]]

    ret = []
    for idx in range(num_periods):
        ret.append(cal)
        cal = cal.previous()
    return ret
