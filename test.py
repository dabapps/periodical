# coding: utf-8

import datetime
import periodical
import unittest


class TestPeriodical(unittest.TestCase):
    def test_daily(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date)
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 1, 1))

    def test_weekly(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date, period='weekly')
        self.assertEqual(cal.start, datetime.date(1999, 12, 27))
        self.assertEqual(cal.end, datetime.date(2000, 1, 2))

    def test_monthly(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date, period='monthly')
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 1, 31))

    def test_quarterly(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date, period='quarterly')
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 3, 31))

    def test_yearly(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date, period='yearly')
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 12, 31))

    # Tests for .previous()

    def test_daily_previous(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date).previous()
        self.assertEqual(cal.start, datetime.date(1999, 12, 31))
        self.assertEqual(cal.end, datetime.date(1999, 12, 31))

    def test_weekly_previous(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date, period='weekly').previous()
        self.assertEqual(cal.start, datetime.date(1999, 12, 20))
        self.assertEqual(cal.end, datetime.date(1999, 12, 26))

    def test_monthly_previous(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date, period='monthly').previous()
        self.assertEqual(cal.start, datetime.date(1999, 12, 1))
        self.assertEqual(cal.end, datetime.date(1999, 12, 31))

        date = datetime.date(2000, 3, 1)
        cal = periodical.CalendarPeriod(date, period='monthly').previous()
        self.assertEqual(cal.start, datetime.date(2000, 2, 1))
        self.assertEqual(cal.end, datetime.date(2000, 2, 29))

    def test_quarterly_previous(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date, period='quarterly').previous()
        self.assertEqual(cal.start, datetime.date(1999, 10, 1))
        self.assertEqual(cal.end, datetime.date(1999, 12, 31))

        date = datetime.date(2000, 4, 1)
        cal = periodical.CalendarPeriod(date, period='quarterly')
        cal = periodical.CalendarPeriod(date, period='quarterly').previous()
        self.assertEqual(cal.start, datetime.date(2000, 1, 1))
        self.assertEqual(cal.end, datetime.date(2000, 3, 31))

    def test_yearly_previous(self):
        date = datetime.date(2000, 1, 1)
        cal = periodical.CalendarPeriod(date, period='yearly').previous()
        self.assertEqual(cal.start, datetime.date(1999, 1, 1))
        self.assertEqual(cal.end, datetime.date(1999, 12, 31))

    # Tests for isoformats

    def test_daily_series(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.get_periods_descending(date, 'daily', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01-01', '1999-12-31', '1999-12-30'], iso)

    def test_weekly_series(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.get_periods_descending(date, 'weekly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['1999-W52', '1999-W51', '1999-W50'], iso)

    def test_monthly_series(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.get_periods_descending(date, 'monthly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01', '1999-12', '1999-11'], iso)

    def test_quarterly_series(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.get_periods_descending(date, 'quarterly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000-01', '1999-10', '1999-07'], iso)

    def test_yearly_series(self):
        date = datetime.date(2000, 1, 1)
        periods = periodical.get_periods_descending(date, 'yearly', 3)
        iso = [period.isoformat() for period in periods]
        self.assertEqual(['2000', '1999', '1998'], iso)

    # Tests for bad values

    def test_invalid_period(self):
        with self.assertRaises(ValueError):
            date = datetime.date(2000, 1, 1)
            periodical.CalendarPeriod(date, period='blibble')


if __name__ == '__main__':
    unittest.main()
