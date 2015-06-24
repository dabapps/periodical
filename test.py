# coding: utf-8

import collections
import datetime
import periodical
import unittest


class TestDatePeriods(unittest.TestCase):

    # Date/period initialization tests
    def test_daily(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='daily')
        self.assertEqual(period.start, datetime.date(2000, 1, 1))
        self.assertEqual(period.end, datetime.date(2000, 1, 1))

    def test_weekly(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='weekly')
        self.assertEqual(period.start, datetime.date(1999, 12, 27))
        self.assertEqual(period.end, datetime.date(2000, 1, 2))

    def test_monthly(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='monthly')
        self.assertEqual(period.start, datetime.date(2000, 1, 1))
        self.assertEqual(period.end, datetime.date(2000, 1, 31))

    def test_quarterly(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='quarterly')
        self.assertEqual(period.start, datetime.date(2000, 1, 1))
        self.assertEqual(period.end, datetime.date(2000, 3, 31))

    def test_yearly(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='yearly')
        self.assertEqual(period.start, datetime.date(2000, 1, 1))
        self.assertEqual(period.end, datetime.date(2000, 12, 31))

    # Representation initialization tests
    def test_daily_repr(self):
        period = periodical.DatePeriod('2000-01-01')
        self.assertEqual(period.start, datetime.date(2000, 1, 1))
        self.assertEqual(period.end, datetime.date(2000, 1, 1))

    def test_weekly_repr(self):
        period = periodical.DatePeriod('2000-W1')
        self.assertEqual(period.start, datetime.date(2000, 1, 3))
        self.assertEqual(period.end, datetime.date(2000, 1, 9))

    def test_monthly_repr(self):
        period = periodical.DatePeriod('2000-01')
        self.assertEqual(period.start, datetime.date(2000, 1, 1))
        self.assertEqual(period.end, datetime.date(2000, 1, 31))

    def test_quarterly_repr(self):
        period = periodical.DatePeriod('2000-Q1')
        self.assertEqual(period.start, datetime.date(2000, 1, 1))
        self.assertEqual(period.end, datetime.date(2000, 3, 31))

    def test_yearly_repr(self):
        period = periodical.DatePeriod('2000')
        self.assertEqual(period.start, datetime.date(2000, 1, 1))
        self.assertEqual(period.end, datetime.date(2000, 12, 31))

    # Tests for `.previous()`
    def test_daily_previous(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='daily').previous()
        self.assertEqual(period.start, datetime.date(1999, 12, 31))
        self.assertEqual(period.end, datetime.date(1999, 12, 31))

    def test_weekly_previous(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='weekly').previous()
        self.assertEqual(period.start, datetime.date(1999, 12, 20))
        self.assertEqual(period.end, datetime.date(1999, 12, 26))

    def test_monthly_previous(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='monthly').previous()
        self.assertEqual(period.start, datetime.date(1999, 12, 1))
        self.assertEqual(period.end, datetime.date(1999, 12, 31))

        date = datetime.date(2000, 3, 1)
        period = periodical.DatePeriod(date=date, span='monthly').previous()
        self.assertEqual(period.start, datetime.date(2000, 2, 1))
        self.assertEqual(period.end, datetime.date(2000, 2, 29))

    def test_quarterly_previous(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='quarterly').previous()
        self.assertEqual(period.start, datetime.date(1999, 10, 1))
        self.assertEqual(period.end, datetime.date(1999, 12, 31))

        date = datetime.date(2000, 4, 1)
        period = periodical.DatePeriod(date=date, span='quarterly')
        period = periodical.DatePeriod(date=date, span='quarterly').previous()
        self.assertEqual(period.start, datetime.date(2000, 1, 1))
        self.assertEqual(period.end, datetime.date(2000, 3, 31))

    def test_yearly_previous(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='yearly').previous()
        self.assertEqual(period.start, datetime.date(1999, 1, 1))
        self.assertEqual(period.end, datetime.date(1999, 12, 31))

    # Tests for `.next()`
    def test_daily_next(self):
        date = datetime.date(2000, 1, 31)
        period = periodical.DatePeriod(date=date, span='daily').next()
        self.assertEqual(period.start, datetime.date(2000, 2, 1))
        self.assertEqual(period.end, datetime.date(2000, 2, 1))

    def test_weekly_next(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='weekly').next()
        self.assertEqual(period.start, datetime.date(2000, 1, 3))
        self.assertEqual(period.end, datetime.date(2000, 1, 9))

    def test_monthly_next(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='monthly').next()
        self.assertEqual(period.start, datetime.date(2000, 2, 1))
        self.assertEqual(period.end, datetime.date(2000, 2, 29))

        date = datetime.date(2000, 12, 1)
        period = periodical.DatePeriod(date=date, span='monthly').next()
        self.assertEqual(period.start, datetime.date(2001, 1, 1))
        self.assertEqual(period.end, datetime.date(2001, 1, 31))

    def test_quarterly_next(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='quarterly').next()
        self.assertEqual(period.start, datetime.date(2000, 4, 1))
        self.assertEqual(period.end, datetime.date(2000, 6, 30))

        date = datetime.date(2000, 10, 1)
        period = periodical.DatePeriod(date=date, span='quarterly')
        period = periodical.DatePeriod(date=date, span='quarterly').next()
        self.assertEqual(period.start, datetime.date(2001, 1, 1))
        self.assertEqual(period.end, datetime.date(2001, 3, 31))

    def test_yearly_next(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='yearly').next()
        self.assertEqual(period.start, datetime.date(2001, 1, 1))
        self.assertEqual(period.end, datetime.date(2001, 12, 31))

    # Tests for date_periods_descending(), and isoformat representations
    def test_daily_series_descending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.date_periods_descending(date, 'daily', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01-01', '1999-12-31', '1999-12-30'], iso)

    def test_weekly_series_descending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.date_periods_descending(date, 'weekly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['1999-W52', '1999-W51', '1999-W50'], iso)

    def test_monthly_series_descending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.date_periods_descending(date, 'monthly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01', '1999-12', '1999-11'], iso)

    def test_quarterly_series_descending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.date_periods_descending(date, 'quarterly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01', '1999-10', '1999-07'], iso)

    def test_yearly_series_descending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.date_periods_descending(date, 'yearly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000', '1999', '1998'], iso)

    # Tests for date_periods_ascending(), and string representations
    def test_daily_series_ascending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.date_periods_ascending(date, 'daily', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000-01-01', '2000-01-02', '2000-01-03'], reprs)

    def test_weekly_series_ascending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.date_periods_ascending(date, 'weekly', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['1999-W52', '2000-W01', '2000-W02'], reprs)

    def test_monthly_series_ascending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.date_periods_ascending(date, 'monthly', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000-01', '2000-02', '2000-03'], reprs)

    def test_quarterly_series_ascending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.date_periods_ascending(date, 'quarterly', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000-Q1', '2000-Q2', '2000-Q3'], reprs)

    def test_yearly_series_ascending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.date_periods_ascending(date, 'yearly', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000', '2001', '2002'], reprs)

    # Tests for date_periods_between
    def test_yearly_series_between_dates(self):
        date_from = datetime.date(2000, 1, 1)
        date_until = datetime.date(2002, 1, 1)

        periods = periodical.date_periods_between(date_from, date_until, 'yearly')
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000', '2001', '2002'], reprs)

        periods = periodical.date_periods_between(date_until, date_from, 'yearly')
        reprs = [str(period) for period in periods]
        self.assertEqual(['2002', '2001', '2000'], reprs)

        periods = periodical.date_periods_between(date_from, date_from, 'yearly')
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000'], reprs)

    # Test using the current day instead of explicitly specifying
    def test_today_func(self):
        def today():
            return datetime.date(2000, 1, 1)
        cal = periodical.DatePeriod(span='monthly', _today_func=today)
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 1, 31))

    def test_default_today(self):
        # Simply exersize the default `today` implementation
        period = periodical.DatePeriod(span='yearly')
        period_repr = str(period)
        self.assertEqual(len(period_repr), 4)

    def test_repr(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.DatePeriod(date=date, span='monthly')
        self.assertEqual(repr(cal), "<DatePeriod '2000-01'>")

    # Tests for bad values
    def test_invalid_period(self):
        date = datetime.date(2000, 1, 1)
        with self.assertRaises(ValueError):
            periodical.DatePeriod(date=date, span='blibble')

    def test_invalid_date_period_comparison(self):
        date = datetime.date(2000, 1, 1)
        period = periodical.DatePeriod(date=date, span='day')
        self.assertFalse(period == 5)

    def test_invalid_time_period_comparison(self):
        time = datetime.datetime(2000, 1, 1, 0, 0, 0)
        period = periodical.TimePeriod(time=time, span='day')
        self.assertFalse(period == 5)

    def test_unknown_representation(self):
        with self.assertRaises(ValueError):
            periodical.DatePeriod('199x')

    def test_map(self):
        date = datetime.date(2014, 9, 1)
        periods = periodical.date_periods_ascending(date=date, span='monthly', num_periods=4)
        date_value_pairs = [
            (datetime.date(2014, 9, 1), 20),
            (datetime.date(2014, 9, 2), 25),
            (datetime.date(2014, 10, 1), 20),
            (datetime.date(2014, 10, 1), 20),
            (datetime.date(2014, 12, 1), 30),
        ]
        mapped = periodical.map(periods, date_value_pairs)
        expected = collections.OrderedDict([
            (periodical.DatePeriod('2014-09'), [20, 25]),
            (periodical.DatePeriod('2014-10'), [20, 20]),
            (periodical.DatePeriod('2014-11'), []),
            (periodical.DatePeriod('2014-12'), [30]),
        ])
        self.assertEqual(mapped, expected)

    def test_summation(self):
        date = datetime.date(2014, 9, 1)
        periods = periodical.date_periods_ascending(date=date, span='monthly', num_periods=4)
        date_value_pairs = [
            (datetime.date(2014, 9, 1), 20),
            (datetime.date(2014, 9, 2), 25),
            (datetime.date(2014, 10, 1), 20),
            (datetime.date(2014, 10, 1), 20),
            (datetime.date(2014, 12, 1), 30),
        ]
        summed = periodical.summation(periods, date_value_pairs)
        expected = collections.OrderedDict([
            (periodical.DatePeriod('2014-09'), 45),
            (periodical.DatePeriod('2014-10'), 40),
            (periodical.DatePeriod('2014-11'), 0),
            (periodical.DatePeriod('2014-12'), 30),
        ])
        self.assertEqual(summed, expected)

    def test_average(self):
        date = datetime.date(2014, 9, 1)
        periods = periodical.date_periods_ascending(date=date, span='monthly', num_periods=4)
        date_value_pairs = [
            (datetime.date(2014, 9, 1), 20),
            (datetime.date(2014, 9, 2), 25),
            (datetime.date(2014, 10, 1), 20),
            (datetime.date(2014, 10, 1), 20),
            (datetime.date(2014, 12, 1), 30),
        ]
        averages = periodical.average(periods, date_value_pairs)
        expected = collections.OrderedDict([
            (periodical.DatePeriod('2014-09'), 22.5),
            (periodical.DatePeriod('2014-10'), 20.0),
            (periodical.DatePeriod('2014-11'), None),
            (periodical.DatePeriod('2014-12'), 30.0),
        ])
        self.assertEqual(averages, expected)

    def test_count(self):
        date = datetime.date(2014, 9, 1)
        periods = periodical.date_periods_ascending(date=date, span='monthly', num_periods=4)
        dates = [
            datetime.date(2014, 9, 1),
            datetime.date(2014, 9, 2),
            datetime.date(2014, 10, 1),
            datetime.date(2014, 10, 1),
            datetime.date(2014, 12, 1),
        ]
        counts = periodical.count(periods, dates)
        expected = collections.OrderedDict([
            (periodical.DatePeriod('2014-09'), 2),
            (periodical.DatePeriod('2014-10'), 2),
            (periodical.DatePeriod('2014-11'), 0),
            (periodical.DatePeriod('2014-12'), 1),
        ])
        self.assertEqual(counts, expected)


class TestTimePeriods(unittest.TestCase):
    # Date/period initialization tests
    def test_daily(self):
        time = datetime.datetime(2000, 1, 1, 23, 59)
        period = periodical.TimePeriod(time=time, span='daily')
        self.assertEqual(period.start, datetime.datetime(2000, 1, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 2))

    def test_weekly(self):
        time = datetime.datetime(2000, 1, 1, 23, 59)
        period = periodical.TimePeriod(time=time, span='weekly')
        self.assertEqual(period.start, datetime.datetime(1999, 12, 27))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 3))

    def test_monthly(self):
        time = datetime.datetime(2000, 1, 1, 23, 59)
        period = periodical.TimePeriod(time=time, span='monthly')
        self.assertEqual(period.start, datetime.datetime(2000, 1, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 2, 1))

    def test_quarterly(self):
        time = datetime.datetime(2000, 1, 1, 23, 59)
        period = periodical.TimePeriod(time=time, span='quarterly')
        self.assertEqual(period.start, datetime.datetime(2000, 1, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 4, 1))

    def test_yearly(self):
        time = datetime.datetime(2000, 1, 1, 23, 59)
        period = periodical.TimePeriod(time=time, span='yearly')
        self.assertEqual(period.start, datetime.datetime(2000, 1, 1))
        self.assertEqual(period.end, datetime.datetime(2001, 1, 1))

    # Representation initialization tests
    def test_second_repr(self):
        period = periodical.TimePeriod('2000-01-01T23:59:59')
        self.assertEqual(period.start, datetime.datetime(2000, 1, 1, 23, 59, 59))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 2, 0, 0, 0))

    def test_minute_repr(self):
        period = periodical.TimePeriod('2000-01-01T23:59')
        self.assertEqual(period.start, datetime.datetime(2000, 1, 1, 23, 59, 0))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 2, 0, 0, 0))

    def test_hour_repr(self):
        period = periodical.TimePeriod('2000-01-01T23')
        self.assertEqual(period.start, datetime.datetime(2000, 1, 1, 23, 0, 0))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 2, 0, 0, 0))

    def test_daily_repr(self):
        period = periodical.TimePeriod('2000-01-01')
        self.assertEqual(period.start, datetime.datetime(2000, 1, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 2))

    def test_weekly_repr(self):
        period = periodical.TimePeriod('2000-W1')
        self.assertEqual(period.start, datetime.datetime(2000, 1, 3))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 10))

    def test_monthly_repr(self):
        period = periodical.TimePeriod('2000-01')
        self.assertEqual(period.start, datetime.datetime(2000, 1, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 2, 1))

    def test_quarterly_repr(self):
        period = periodical.TimePeriod('2000-Q1')
        self.assertEqual(period.start, datetime.datetime(2000, 1, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 4, 1))

    def test_yearly_repr(self):
        period = periodical.TimePeriod('2000')
        self.assertEqual(period.start, datetime.datetime(2000, 1, 1))
        self.assertEqual(period.end, datetime.datetime(2001, 1, 1))

    def test_utc_repr(self):
        period = periodical.TimePeriod('2000-01Z')
        self.assertEqual(period.start, periodical.utc_datetime(2000, 1, 1))
        self.assertEqual(period.end, periodical.utc_datetime(2000, 2, 1))

    def test_utc_offset_repr(self):
        period = periodical.TimePeriod('2000-01+00:00')
        self.assertEqual(period.start, periodical.utc_datetime(2000, 1, 1))
        self.assertEqual(period.end, periodical.utc_datetime(2000, 2, 1))

    def test_fixed_offset_repr(self):
        period = periodical.TimePeriod('2000-01+01:00')
        self.assertEqual(period.start, datetime.datetime(2000, 1, 1, tzinfo=periodical.Offset('+01:00')))
        self.assertEqual(period.end, datetime.datetime(2000, 2, 1, tzinfo=periodical.Offset('+01:00')))
        self.assertTrue(period.contains(periodical.utc_datetime(2000, 1, 1)))
        self.assertFalse(period.contains(periodical.utc_datetime(2000, 2, 1)))

    # Tests for `.previous()`
    def test_seconds_previous(self):
        time = datetime.datetime(2000, 1, 31, 23, 59, 59)
        period = periodical.TimePeriod(time=time, span='seconds').previous()
        self.assertEqual(period.start, datetime.datetime(2000, 1, 31, 23, 59, 58))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 31, 23, 59, 59))

    def test_minutes_previous(self):
        time = datetime.datetime(2000, 1, 31, 23, 59)
        period = periodical.TimePeriod(time=time, span='minutes').previous()
        self.assertEqual(period.start, datetime.datetime(2000, 1, 31, 23, 58, 0))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 31, 23, 59, 0))

    def test_hourly_previous(self):
        time = datetime.datetime(2000, 1, 31, 23, 00)
        period = periodical.TimePeriod(time=time, span='hour').previous()
        self.assertEqual(period.start, datetime.datetime(2000, 1, 31, 22, 0, 0))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 31, 23, 0, 0))

    def test_daily_previous(self):
        time = datetime.datetime(2000, 1, 1)
        period = periodical.TimePeriod(time=time, span='daily').previous()
        self.assertEqual(period.start, datetime.datetime(1999, 12, 31))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 1))

    def test_weekly_previous(self):
        time = datetime.datetime(2000, 1, 1)
        period = periodical.TimePeriod(time=time, span='weekly').previous()
        self.assertEqual(period.start, datetime.datetime(1999, 12, 20))
        self.assertEqual(period.end, datetime.datetime(1999, 12, 27))

    def test_monthly_previous(self):
        time = datetime.datetime(2000, 1, 1)
        period = periodical.TimePeriod(time=time, span='monthly').previous()
        self.assertEqual(period.start, datetime.datetime(1999, 12, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 1))

        time = datetime.datetime(2000, 3, 1)
        period = periodical.TimePeriod(time=time, span='monthly').previous()
        self.assertEqual(period.start, datetime.datetime(2000, 2, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 3, 1))

    def test_quarterly_previous(self):
        time = datetime.datetime(2000, 1, 1)
        period = periodical.TimePeriod(time=time, span='quarterly').previous()
        self.assertEqual(period.start, datetime.datetime(1999, 10, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 1))

        time = datetime.datetime(2000, 4, 1)
        period = periodical.TimePeriod(time=time, span='quarterly')
        period = periodical.TimePeriod(time=time, span='quarterly').previous()
        self.assertEqual(period.start, datetime.datetime(2000, 1, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 4, 1))

    def test_yearly_previous(self):
        time = datetime.datetime(2000, 1, 1)
        period = periodical.TimePeriod(time=time, span='yearly').previous()
        self.assertEqual(period.start, datetime.datetime(1999, 1, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 1))

    # Tests for `.next()`
    def test_seconds_next(self):
        time = datetime.datetime(2000, 1, 31, 23, 59, 59)
        period = periodical.TimePeriod(time=time, span='seconds').next()
        self.assertEqual(period.start, datetime.datetime(2000, 2, 1, 0, 0, 0))
        self.assertEqual(period.end, datetime.datetime(2000, 2, 1, 0, 0, 1))

    def test_minutes_next(self):
        time = datetime.datetime(2000, 1, 31, 23, 59)
        period = periodical.TimePeriod(time=time, span='minutes').next()
        self.assertEqual(period.start, datetime.datetime(2000, 2, 1, 0, 0))
        self.assertEqual(period.end, datetime.datetime(2000, 2, 1, 0, 1))

    def test_hourly_next(self):
        time = datetime.datetime(2000, 1, 31, 23, 00)
        period = periodical.TimePeriod(time=time, span='hour').next()
        self.assertEqual(period.start, datetime.datetime(2000, 2, 1, 0))
        self.assertEqual(period.end, datetime.datetime(2000, 2, 1, 1))

    def test_daily_next(self):
        time = datetime.datetime(2000, 1, 31)
        period = periodical.TimePeriod(time=time, span='daily').next()
        self.assertEqual(period.start, datetime.datetime(2000, 2, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 2, 2))

    def test_weekly_next(self):
        time = datetime.datetime(2000, 1, 1)
        period = periodical.TimePeriod(time=time, span='weekly').next()
        self.assertEqual(period.start, datetime.datetime(2000, 1, 3))
        self.assertEqual(period.end, datetime.datetime(2000, 1, 10))

    def test_monthly_next(self):
        time = datetime.datetime(2000, 1, 1)
        period = periodical.TimePeriod(time=time, span='monthly').next()
        self.assertEqual(period.start, datetime.datetime(2000, 2, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 3, 1))

        time = datetime.datetime(2000, 12, 1)
        period = periodical.TimePeriod(time=time, span='monthly').next()
        self.assertEqual(period.start, datetime.datetime(2001, 1, 1))
        self.assertEqual(period.end, datetime.datetime(2001, 2, 1))

    def test_quarterly_next(self):
        time = datetime.datetime(2000, 1, 1)
        period = periodical.TimePeriod(time=time, span='quarterly').next()
        self.assertEqual(period.start, datetime.datetime(2000, 4, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 7, 1))

        time = datetime.datetime(2000, 10, 1)
        period = periodical.TimePeriod(time=time, span='quarterly')
        period = periodical.TimePeriod(time=time, span='quarterly').next()
        self.assertEqual(period.start, datetime.datetime(2001, 1, 1))
        self.assertEqual(period.end, datetime.datetime(2001, 4, 1))

    def test_yearly_next(self):
        time = datetime.datetime(2000, 1, 1)
        period = periodical.TimePeriod(time=time, span='yearly').next()
        self.assertEqual(period.start, datetime.datetime(2001, 1, 1))
        self.assertEqual(period.end, datetime.datetime(2002, 1, 1))

    # Tests for date_periods_descending(), and isoformat representations
    def test_offset_second_series_descending(self):
        time = datetime.datetime(2000, 1, 1, 23, 00, 00, tzinfo=periodical.Offset('+01:30'))
        periods = periodical.time_periods_descending(time, 'seconds', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01-01T23:00:00+01:30', '2000-01-01T22:59:59+01:30', '2000-01-01T22:59:58+01:30'], iso)

    def test_offset_minute_series_descending(self):
        time = datetime.datetime(2000, 1, 1, 23, 00, tzinfo=periodical.Offset('-01:30'))
        periods = periodical.time_periods_descending(time, 'minutes', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01-01T23:00-01:30', '2000-01-01T22:59-01:30', '2000-01-01T22:58-01:30'], iso)

    def test_utc_hourly_series_descending(self):
        time = periodical.utc_datetime(2000, 1, 1, 1)
        periods = periodical.time_periods_descending(time, 'hourly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01-01T01:00Z', '2000-01-01T00:00Z', '1999-12-31T23:00Z'], iso)

    def test_daily_series_descending(self):
        time = datetime.datetime(2000, 1, 1)
        periods = periodical.time_periods_descending(time, 'daily', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01-01', '1999-12-31', '1999-12-30'], iso)

    def test_weekly_series_descending(self):
        time = datetime.datetime(2000, 1, 1)
        periods = periodical.date_periods_descending(time, 'weekly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['1999-W52', '1999-W51', '1999-W50'], iso)

    def test_monthly_series_descending(self):
        time = datetime.datetime(2000, 1, 1)
        periods = periodical.date_periods_descending(time, 'monthly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01', '1999-12', '1999-11'], iso)

    def test_quarterly_series_descending(self):
        time = datetime.datetime(2000, 1, 1)
        periods = periodical.date_periods_descending(time, 'quarterly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01', '1999-10', '1999-07'], iso)

    def test_yearly_series_descending(self):
        time = datetime.datetime(2000, 1, 1)
        periods = periodical.date_periods_descending(time, 'yearly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000', '1999', '1998'], iso)

    # Tests for date_periods_ascending(), and string representations
    def test_daily_series_ascending(self):
        time = datetime.datetime(2000, 1, 1)
        periods = periodical.time_periods_ascending(time, 'daily', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000-01-01', '2000-01-02', '2000-01-03'], reprs)

    def test_weekly_series_ascending(self):
        time = datetime.datetime(2000, 1, 1)
        periods = periodical.time_periods_ascending(time, 'weekly', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['1999-W52', '2000-W01', '2000-W02'], reprs)

    def test_monthly_series_ascending(self):
        time = datetime.datetime(2000, 1, 1)
        periods = periodical.time_periods_ascending(time, 'monthly', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000-01', '2000-02', '2000-03'], reprs)

    def test_quarterly_series_ascending(self):
        time = datetime.datetime(2000, 1, 1)
        periods = periodical.time_periods_ascending(time, 'quarterly', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000-Q1', '2000-Q2', '2000-Q3'], reprs)

    def test_yearly_series_ascending(self):
        time = datetime.datetime(2000, 1, 1)
        periods = periodical.time_periods_ascending(time, 'yearly', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000', '2001', '2002'], reprs)

    # Tests for date_periods_between
    def test_yearly_series_between_dates(self):
        time_from = datetime.datetime(2000, 1, 1)
        time_until = datetime.datetime(2002, 1, 1)

        periods = periodical.time_periods_between(time_from, time_until, 'yearly')
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000', '2001', '2002'], reprs)

        periods = periodical.time_periods_between(time_until, time_from, 'yearly')
        reprs = [str(period) for period in periods]
        self.assertEqual(['2002', '2001', '2000'], reprs)

        periods = periodical.time_periods_between(time_from, time_from, 'yearly')
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000'], reprs)

    # Test using the current time instead of explicitly specifying
    def test_now_func(self):
        def now():
            return datetime.datetime(2000, 1, 1)
        period = periodical.TimePeriod(span='monthly', _now_func=now)
        self.assertEqual(period.start, datetime.datetime(2000, 1, 1))
        self.assertEqual(period.end, datetime.datetime(2000, 2, 1))

    def test_default_now_func_is_timezone_aware(self):
        period = periodical.TimePeriod(span='yearly')
        period_repr = str(period)
        self.assertEqual(len(period_repr), 5)
        self.assertEqual(period_repr[-1], 'Z')

    def test_repr(self):
        time = datetime.datetime(2000, 1, 1)
        cal = periodical.TimePeriod(time=time, span='monthly')
        self.assertEqual(repr(cal), "<TimePeriod '2000-01'>")

    # Tests for bad values
    def test_invalid_period(self):
        time = datetime.datetime(2000, 1, 1)
        with self.assertRaises(ValueError):
            periodical.TimePeriod(time=time, span='blibble')

    def test_unknown_representation(self):
        with self.assertRaises(ValueError):
            periodical.TimePeriod('199x')

    # def test_map(self):
    #     date = datetime.date(2014, 9, 1)
    #     periods = periodical.date_periods_ascending(date=date, span='monthly', num_periods=4)
    #     date_value_pairs = [
    #         (datetime.date(2014, 9, 1), 20),
    #         (datetime.date(2014, 9, 2), 25),
    #         (datetime.date(2014, 10, 1), 20),
    #         (datetime.date(2014, 10, 1), 20),
    #         (datetime.date(2014, 12, 1), 30),
    #     ]
    #     mapped = periodical.map(periods, date_value_pairs)
    #     expected = collections.OrderedDict([
    #         (periodical.DatePeriod('2014-09'), [20, 25]),
    #         (periodical.DatePeriod('2014-10'), [20, 20]),
    #         (periodical.DatePeriod('2014-11'), []),
    #         (periodical.DatePeriod('2014-12'), [30]),
    #     ])
    #     self.assertEqual(mapped, expected)

    # def test_summation(self):
    #     date = datetime.date(2014, 9, 1)
    #     periods = periodical.date_periods_ascending(date=date, span='monthly', num_periods=4)
    #     date_value_pairs = [
    #         (datetime.date(2014, 9, 1), 20),
    #         (datetime.date(2014, 9, 2), 25),
    #         (datetime.date(2014, 10, 1), 20),
    #         (datetime.date(2014, 10, 1), 20),
    #         (datetime.date(2014, 12, 1), 30),
    #     ]
    #     summed = periodical.summation(periods, date_value_pairs)
    #     expected = collections.OrderedDict([
    #         (periodical.DatePeriod('2014-09'), 45),
    #         (periodical.DatePeriod('2014-10'), 40),
    #         (periodical.DatePeriod('2014-11'), 0),
    #         (periodical.DatePeriod('2014-12'), 30),
    #     ])
    #     self.assertEqual(summed, expected)

    # def test_average(self):
    #     date = datetime.date(2014, 9, 1)
    #     periods = periodical.date_periods_ascending(date=date, span='monthly', num_periods=4)
    #     date_value_pairs = [
    #         (datetime.date(2014, 9, 1), 20),
    #         (datetime.date(2014, 9, 2), 25),
    #         (datetime.date(2014, 10, 1), 20),
    #         (datetime.date(2014, 10, 1), 20),
    #         (datetime.date(2014, 12, 1), 30),
    #     ]
    #     averages = periodical.average(periods, date_value_pairs)
    #     expected = collections.OrderedDict([
    #         (periodical.DatePeriod('2014-09'), 22.5),
    #         (periodical.DatePeriod('2014-10'), 20.0),
    #         (periodical.DatePeriod('2014-11'), None),
    #         (periodical.DatePeriod('2014-12'), 30.0),
    #     ])
    #     self.assertEqual(averages, expected)

    def test_count(self):
        time = periodical.utc_datetime(2014, 9, 1)
        periods = periodical.time_periods_ascending(time=time, span='monthly', num_periods=4)
        dates = [
            periodical.utc_datetime(2014, 9, 1),
            periodical.utc_datetime(2014, 9, 2),
            periodical.utc_datetime(2014, 10, 1),
            periodical.utc_datetime(2014, 10, 1),
            periodical.utc_datetime(2014, 12, 1),
        ]
        counts = periodical.count(periods, dates)
        expected = collections.OrderedDict([
            (periodical.TimePeriod('2014-09Z'), 2),
            (periodical.TimePeriod('2014-10Z'), 2),
            (periodical.TimePeriod('2014-11Z'), 0),
            (periodical.TimePeriod('2014-12Z'), 1),
        ])
        self.assertEqual(counts, expected)

if __name__ == '__main__':
    unittest.main()
