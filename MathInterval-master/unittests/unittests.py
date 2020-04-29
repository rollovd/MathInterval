from Elements.exceptions import LimitError, OutTimestamp, ErrorDate, ComparingError
from ITF.DiscreteIntervalTableFunction import DiscreteIntervalTableFunction
from ITF.DiscreteIntervalTableFunctionLimit import DiscreteIntervalTableFunctionLimit
from ITF.IntervalTableFunction import IntervalTableFunction
import unittest
import datetime
import numpy as np
import os

class TestAllMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAllMethods, self).__init__(*args, **kwargs)
        self.year = 2020
        self.month = 1

        self.date_start = datetime.datetime(self.year, self.month, 1, 0, 0)
        self.date_end = datetime.datetime(self.year, self.month, 31, 0, 0)

        self.object_ditf1 = DiscreteIntervalTableFunction(self.date_start, self.date_start)
        self.object_ditf1.add_date(self.date_start, 10)
        self.object_ditf1.add_interval(self.date_start, self.date_start, 10)

        self.object_ditf2 = DiscreteIntervalTableFunction(self.date_start, self.date_end)
        fill_dates_day = [1, 5, 13, 14, 15, 20, 22, 26, 30, 31]
        fill_day_values = [x * 10 for x in fill_dates_day]

        fill_dates_interval = [(2, 4), (3, 8), (10, 10), (15, 21), (1, 2), (30, 31)]
        fill_interval_values = [min(x) * 10 for x in fill_dates_interval]

        for i in range(len(fill_dates_day)):
            current_date = datetime.datetime(self.year, self.month, fill_dates_day[i], 0, 0)
            self.object_ditf2.add_date(current_date, fill_day_values[i])

        for i in range(len(fill_dates_interval)):
            current_date1 = datetime.datetime(self.year, self.month, fill_dates_interval[i][0], 0, 0)
            current_date2 = datetime.datetime(self.year, self.month, fill_dates_interval[i][1], 0, 0)
            self.object_ditf2.add_interval(current_date1, current_date2, fill_interval_values[i])

    def test_shape_coincidence(self):
        self.assertEqual(self.object_ditf1.length_of_storage, 1)
        self.assertEqual(self.object_ditf2.length_of_storage, 31)

    def test_filling_dates_ditf1(self):
        current_index = self.object_ditf1.get_index(self.date_start)
        current_value = self.object_ditf1.get_value(self.date_start)

        self.assertEqual(current_index, 0)
        self.assertEqual(current_value, 20)

    def test_filling_dates_ditf2(self):
        date_check1 = datetime.datetime(self.year, self.month, 8, 0, 0)
        date_check2 = datetime.datetime(self.year, self.month, 31, 0, 0)

        current_index1 = self.object_ditf2.get_index(date_check1)
        current_index2 = self.object_ditf2.get_index(date_check2)
        self.assertEqual(current_index1, 7)
        self.assertEqual(current_index2, 30)

        current_value1 = self.object_ditf2.get_value(date_check1)
        current_value2 = self.object_ditf2.get_value(date_check2)
        self.assertEqual(current_value1, 30)
        self.assertEqual(current_value2, 610)

    def test_get_sum_max_ditf1(self):
        max_day = self.object_ditf1.get_max_interval(self.date_start, self.date_start)
        sum_day = self.object_ditf1.get_sum_interval(self.date_start, self.date_start)
        self.assertEqual(max_day, sum_day)

    def test_get_sum_max_ditf2(self):
        intervals = [(1, 1), (2, 5), (3, 4), (5, 9), (10, 25)]
        answers = [20, 80, 50, 80, 350]

        for interval, answer in zip(intervals, answers):
            start_date = datetime.datetime(2020, 1, interval[0], 0, 0)
            end_date = datetime.datetime(2020, 1, interval[1], 0, 0)

            max_value = self.object_ditf2.get_max_interval(start_date, end_date)
            self.assertEqual(max_value, answer)

    def test_get_intervals_ditf1(self):
        limits = (8, 10, 12)
        answers = [[], [1577826000.0, 1577826000.0], [1577826000.0, 1577826000.0]]

        for limit in limits:
            result = self.object_ditf1.get_intervals(self.date_start, self.date_start, max_limit=limit,
                                                    condition='lower', include=True)
            i = 0
            for res in result:
                self.assertEqual(answers[i], res)

        include_check = self.object_ditf1.get_intervals(self.date_start, self.date_start, max_limit=10,
                                                        condition='lower', include=False)[0]
        self.assertEqual(include_check, [])

    def test_get_intervals_ditf2(self):
        intervals = [(1, 1), (2, 5), (3, 4), (5, 9), (10, 25)]
        limits = [(19, 20, 21), (29, 78, 81), (49, 50, 51), (0, 25, 40), (10, 120, 180)]
        answers = ([], [1577826000.0, 1577826000.0], [1577826000.0, 1577826000.0],
                   [], [1577912400.0, 1578085200.0], [1577912400.0, 1578171600.0],
                   [], [1577998800.0, 1578085200.0], [1577998800.0, 1578085200.0],
                   [1578517200.0, 1578517200.0], [1578517200.0, 1578517200.0], [1578258000.0, 1578517200.0],
                   [1578690000.0, 1578776400.0], [1579726800.0, 1579899600.0], [1578603600.0, 1578776400.0],
                   [1579726800.0, 1579899600.0], [1578603600.0, 1578949200.0], [1579122000.0, 1579381200.0],
                   [1579554000.0, 1579554000.0], [1579726800.0, 1579899600.0])

        i = 0
        for interval, current_limits in zip(intervals, limits):
            start_date = datetime.datetime(2020, 1, interval[0], 0, 0)
            end_date = datetime.datetime(2020, 1, interval[1], 0, 0)

            for limit in current_limits:
                result = self.object_ditf2.get_intervals(start_date, end_date, limit, condition='lower',
                                                         include=True)
                for res in result:
                    self.assertEqual(res, answers[i])
                    i += 1

    def test_check_interval_limit(self):
        intervals = [(1, 1), (2, 5), (3, 4), (5, 9), (10, 25)]
        limits = [20, 80, 50, 0, 20]
        answers = [True, False, True, True, False]

        for interval, limit, answer in zip(intervals, limits, answers):
            start_date = datetime.datetime(2020, 1, interval[0], 0, 0)
            end_date = datetime.datetime(2020, 1, interval[1], 0, 0)

            result = self.object_ditf2.check_interval_limit(start_date, end_date, limit, condition='higher')
            self.assertEqual(result, answer)

    def test_get_days_on_condition(self):
        pass



if __name__ == "__main__":
    unittest.main()