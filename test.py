# coding: utf-8

import datetime
import periodical
import unittest


class TestPeriodical(unittest.TestCase):

    # Date/period initialization tests
    def test_daily(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date=date, period='daily')
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 1, 1))

    def test_weekly(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date=date, period='weekly')
        self.assertEqual(cal.start, datetime.date(1999, 12, 27))
        self.assertEqual(cal.end, datetime.date(2000, 1, 2))

    def test_monthly(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date=date, period='monthly')
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 1, 31))

    def test_quarterly(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date=date, period='quarterly')
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 3, 31))

    def test_yearly(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date=date, period='yearly')
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 12, 31))

    # Representation initialization tests
    def test_daily_repr(self):
        cal = periodical.CalendarPeriod('2000-01-01')
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 1, 1))

    def test_weekly_repr(self):
        cal = periodical.CalendarPeriod('2000-W1')
        self.assertEqual(cal.start, datetime.date(2000, 1, 3))
        self.assertEqual(cal.end, datetime.date(2000, 1, 9))

    def test_monthly_repr(self):
        cal = periodical.CalendarPeriod('2000-01')
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 1, 31))

    def test_quarterly_repr(self):
        cal = periodical.CalendarPeriod('2000-Q1')
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 3, 31))

    def test_yearly_repr(self):
        cal = periodical.CalendarPeriod('2000')
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 12, 31))

    # Tests for `.previous()`
    def test_daily_previous(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date=date, period='daily').previous()
        self.assertEqual(cal.start, datetime.date(1999, 12, 31))
        self.assertEqual(cal.end, datetime.date(1999, 12, 31))

    def test_weekly_previous(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date=date, period='weekly').previous()
        self.assertEqual(cal.start, datetime.date(1999, 12, 20))
        self.assertEqual(cal.end, datetime.date(1999, 12, 26))

    def test_monthly_previous(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date=date, period='monthly').previous()
        self.assertEqual(cal.start, datetime.date(1999, 12, 1))
        self.assertEqual(cal.end, datetime.date(1999, 12, 31))

        date = datetime.date(2000, 3, 1)
        cal = periodical.CalendarPeriod(date=date, period='monthly').previous()
        self.assertEqual(cal.start, datetime.date(2000, 2, 1))
        self.assertEqual(cal.end, datetime.date(2000, 2, 29))

    def test_quarterly_previous(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date=date, period='quarterly').previous()
        self.assertEqual(cal.start, datetime.date(1999, 10, 1))
        self.assertEqual(cal.end, datetime.date(1999, 12, 31))

        date = datetime.date(2000, 4, 1)
        cal = periodical.CalendarPeriod(date=date, period='quarterly')
        cal = periodical.CalendarPeriod(date=date, period='quarterly').previous()
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 3, 31))

    def test_yearly_previous(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date=date, period='yearly').previous()
        self.assertEqual(cal.start, datetime.date(1999, 1, 1))
        self.assertEqual(cal.end, datetime.date(1999, 12, 31))

    # Tests for `.next()`
    def test_daily_next(self):
        date = datetime.date(2000, 1, 31)
        cal = periodical.CalendarPeriod(date=date, period='daily').next()
        self.assertEqual(cal.start, datetime.date(2000, 2, 1))
        self.assertEqual(cal.end, datetime.date(2000, 2, 1))

    def test_weekly_next(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date=date, period='weekly').next()
        self.assertEqual(cal.start, datetime.date(2000, 1, 3))
        self.assertEqual(cal.end, datetime.date(2000, 1, 9))

    def test_monthly_next(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date=date, period='monthly').next()
        self.assertEqual(cal.start, datetime.date(2000, 2, 1))
        self.assertEqual(cal.end, datetime.date(2000, 2, 29))

        date = datetime.date(2000, 12, 1)
        cal = periodical.CalendarPeriod(date=date, period='monthly').next()
        self.assertEqual(cal.start, datetime.date(2001, 1, 1))
        self.assertEqual(cal.end, datetime.date(2001, 1, 31))

    def test_quarterly_next(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date=date, period='quarterly').next()
        self.assertEqual(cal.start, datetime.date(2000, 4, 1))
        self.assertEqual(cal.end, datetime.date(2000, 6, 30))

        date = datetime.date(2000, 10, 1)
        cal = periodical.CalendarPeriod(date=date, period='quarterly')
        cal = periodical.CalendarPeriod(date=date, period='quarterly').next()
        self.assertEqual(cal.start, datetime.date(2001, 1, 1))
        self.assertEqual(cal.end, datetime.date(2001, 3, 31))

    def test_yearly_next(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date=date, period='yearly').next()
        self.assertEqual(cal.start, datetime.date(2001, 1, 1))
        self.assertEqual(cal.end, datetime.date(2001, 12, 31))

    # Tests for periods_descending(), and isoformat representations
    def test_daily_series_descending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.periods_descending(date, 'daily', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01-01', '1999-12-31', '1999-12-30'], iso)

    def test_weekly_series_descending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.periods_descending(date, 'weekly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['1999-W52', '1999-W51', '1999-W50'], iso)

    def test_monthly_series_descending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.periods_descending(date, 'monthly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01', '1999-12', '1999-11'], iso)

    def test_quarterly_series_descending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.periods_descending(date, 'quarterly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01', '1999-10', '1999-07'], iso)

    def test_yearly_series_descending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.periods_descending(date, 'yearly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000', '1999', '1998'], iso)

    # Tests for periods_ascending(), and string representations
    def test_daily_series_ascending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.periods_ascending(date, 'daily', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000-01-01', '2000-01-02', '2000-01-03'], reprs)

    def test_weekly_series_ascending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.periods_ascending(date, 'weekly', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['1999-W52', '2000-W01', '2000-W02'], reprs)

    def test_monthly_series_ascending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.periods_ascending(date, 'monthly', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000-01', '2000-02', '2000-03'], reprs)

    def test_quarterly_series_ascending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.periods_ascending(date, 'quarterly', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000-Q1', '2000-Q2', '2000-Q3'], reprs)

    def test_yearly_series_ascending(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.periods_ascending(date, 'yearly', 3)
        reprs = [str(period) for period in periods]
        self.assertEqual(['2000', '2001', '2002'], reprs)

    # Tests for bad values
    def test_invalid_period(self):
        date = datetime.date(2000, 1, 1)
        with self.assertRaises(ValueError):
            periodical.CalendarPeriod(date=date, period='blibble')

    def test_unknown_representation(self):
        with self.assertRaises(ValueError):
            periodical.CalendarPeriod('199x')

if __name__ == '__main__':
    unittest.main()
