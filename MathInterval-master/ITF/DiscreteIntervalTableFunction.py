import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from Elements.exceptions import ErrorDate, OutTimestamp, ComparingError, IncorrectIntervalError
from ITF.Interval import Interval

class DiscreteIntervalTableFunction:
    def __init__(self, *args):
        self.__initialize_dates(args)
        self.__step = 86400
        if self.start_date <= self.end_date:
            self.all_days = self.__zeros_vector(self.start_date, self.end_date)
            self.length_of_storage = self.all_days.shape[0]

        else:
            raise IncorrectIntervalError(self.start_date, self.end_date)

    def __initialize_dates(self, args):
        if len(args) == 1:
            if isinstance(args[0], Interval):
                self.start_date = args[0].start_date
                self.end_date = args[0].end_date
            else:
                raise ValueError('Incorrect input')

        elif len(args) == 2:
            if all(type(i) is datetime.datetime for i in args):
                self.start_date = self.__check_type_of_date(args[0])
                self.end_date = self.__check_type_of_date(args[1])
            else:
                raise ValueError('Incorrect input')
        else:
            raise ValueError('Incorrect input')

    @staticmethod
    def comparing_dates(date_start, date_end):
        if date_end >= date_start:
            return True
        else:
            raise ComparingError(date_start, date_end)

    def get_value(self, date):
        """Возвращает значение хранения по указанной в аргументе дате"""
        timestamp = self.__check_type_of_date(date)
        index = self.get_index(timestamp)
        return self.all_days[index]

    def get_index(self, date):
        """Возвращает индекс даты в списке all_days"""
        timestamp = self.__check_type_of_date(date)
        index = int((timestamp - self.start_date) / self.__step)

        if index >= self.length_of_storage or index < 0:
            raise OutTimestamp(timestamp, self.start_date, self.end_date)
        else:
            return index

    def __zeros_vector(self, timestamp1, timestamp2):
        """Создание нулевого вектора"""
        qty_days = self.__quantity_days(timestamp1, timestamp2)
        zeros_vector = np.zeros(qty_days)
        return zeros_vector

    def __quantity_days(self, timestamp1, timestamp2):
        """Количество дней между начальной и конечной датой (включительно)"""
        return int((timestamp2 - timestamp1) / self.__step) + 1

    @staticmethod
    def convert_to_timestamp(date):
        """Конвертирует дату формата datetime.datetime в timestamp"""
        return date.timestamp()

    @staticmethod
    def from_timestamp(timestamp_value):
        """Конвертирует timestamp в datetime.datetime формата YYYY/MM/DD"""
        get_date = datetime.datetime.fromtimestamp(timestamp_value).strftime('%Y/%m/%d')
        return get_date

    def __check_type_of_date(self, date):
        """Проверка корректности входных данных"""
        if isinstance(date, float):
            return date
        else:
            return self.convert_to_timestamp(date)

    def add_date(self, date, value):
        """Добавление значения хранения для заданной даты"""
        index = self.get_index(date)
        self.all_days[index] += value

    def add_interval(self, start_date, end_date, value):
        """Добавление значения хранения для интервала дат"""
        if self.comparing_dates(start_date, end_date):
            pass

        ix1 = self.get_index(start_date)
        ix2 = self.get_index(end_date)

        self.all_days[ix1: ix2 + 1] += value

    def check_date_intervals(self, array):
        """Конвертирование вектора timestamp дат в вектор дат формата YYYY/MM/DD"""
        try:
            vectorize_timestamp = np.vectorize(lambda x: self.from_timestamp(x))
            return vectorize_timestamp(array).tolist()
        except ValueError:
            raise ValueError('Your array is empty.')

    def __cut_array(self, start_date, end_date, indexes=False):
        """Срез вектора относительно введённых дат начала и конца интервала"""
        ix1 = self.get_index(start_date)
        ix2 = self.get_index(end_date) + 1
        cut_days = self.all_days[ix1: ix2]

        if indexes:
            return cut_days, ix1, ix2
        else:
            return cut_days

    def __convert_to_date(self, array):
        """Перевод из индексов в timestamp"""
        vectorize_func = np.vectorize(lambda ix: ix * self.__step + self.start_date)
        return vectorize_func(array)

    def get_max_interval(self, start_date, end_date):
        """Получение максимального значения на интервале дат"""
        if self.comparing_dates(start_date, end_date):
            pass

        cut_days = self.__cut_array(start_date, end_date)
        return max(cut_days)

    def get_sum_interval(self, start_date, end_date):
        """Получение суммы значений на интервале дат"""
        if self.comparing_dates(start_date, end_date):
            pass

        cut_days = self.__cut_array(start_date, end_date)
        return sum(cut_days)

    def get_graph(self, start_date, end_date, name_save=None):
        """Визуализация величин хранения на определённом интервале дат"""
        if self.comparing_dates(start_date, end_date):
            pass

        plt.figure(figsize=(15, 10))

        cut_days, ix1, ix2 = self.__cut_array(start_date, end_date, indexes=True)
        x_timestamp = self.__convert_to_date(list(range(ix1, ix2)))

        xaxis = np.hstack([np.repeat(self.from_timestamp(timestamp), 2) for timestamp in x_timestamp])
        yaxis = np.hstack([np.array([0.0, value_day]) for value_day in cut_days])

        sns_plot = sns.pointplot(xaxis, yaxis, join=False)

        plt.xlabel('Date')
        plt.ylabel('Limit')
        plt.xticks(rotation=45)

        if name_save:
            sns_plot.figure.savefig(f'{name_save}.png')

    def __getting_intervals(self, start_date, end_date, max_limit, condition='higher', include=True):
        """Возвращает индексы валидных периодов на основе входных параметров"""
        cut_days, ix1, ix2 = self.__cut_array(start_date, end_date, indexes=True)

        intervals = []
        current = []
        for i in range(len(cut_days)):
            if self.__set_sign_on_conditions(cut_days[i], max_limit, condition=condition, include=include):
                if not current:
                    current.append(i + ix1)
                if current and i == len(cut_days) - 1:
                    current.append(i + ix1)
                    intervals.append(current)
            else:
                if current:
                    current.append(i + ix1 - 1)
                    intervals.append(current)
                    current = []

        return intervals

    def __set_sign_on_conditions(self, value1, value2, condition='lower', include=True):
        """Определение знака сравнения на основе параметров"""
        if condition == 'lower' and include:
            return value1 <= value2
        elif condition == 'lower' and not include:
            return value1 < value2
        elif condition == 'higher' and include:
            return value1 >= value2
        elif condition == 'higher' and not include:
            return value1 > value2
        else:
            raise ValueError(f"Your condition '{condition}' doesn't exist or variable 'include' is not bool type")

    def get_intervals(self, start_date, end_date, max_limit, condition='lower', include=True):
        """Возвращает валидные периоды на основе входных параметров"""
        if self.comparing_dates(start_date, end_date):
            pass

        intervals = self.__getting_intervals(start_date, end_date, max_limit, condition, include)

        if not intervals:
            return [[]]
        else:
            intervals = self.__convert_to_date(intervals)
            return intervals.tolist()

    def get_days_on_condition(self, start_date, end_date, max_limit, occurrence='left', condition='lower',
                              include=True, quantity_days=1):
        """Возвращает интервал первых/последних вхождений валидных дат на основе входных параметров"""
        if self.comparing_dates(start_date, end_date):
            pass

        intervals = self.__getting_intervals(start_date, end_date, max_limit, condition, include)

        if not intervals:
            raise ErrorDate(start_date, end_date, max_limit, occurrence, condition, include)

        else:
            intervals = self.__convert_to_date(intervals).tolist()
            key = 1 if occurrence == 'left' else -1 if occurrence == 'right' else None

            if key:
                intervals = intervals[::key]
                result = []

                for i in range(len(intervals)):
                    period = intervals[i]
                    qty_days_current = self.__quantity_days(period[0], period[-1])

                    if quantity_days <= qty_days_current:
                        timestamp_start = period[::key][0]
                        timestamp_end = timestamp_start + key * (quantity_days - 1) * self.__step
                        result.extend([timestamp_start, timestamp_end])
                        break

                return result[::key]

            else:
                raise ValueError(f"Your occurrence '{occurrence}' doesn't exist.")

    # def raw_get_days_on_condition(self, start_date, end_date, max_limit, occurrence='left', condition='lower',
    #                               include=True, quantity_days=1):
    #     """Возвращает интервал первых/последних вхождений валидных дат на основе входных параметров"""
    #     if self.comparing_dates(start_date, end_date):
    #         pass
    #
    #     intervals = self.__getting_intervals(start_date, end_date, max_limit, condition, include)
    #
    #     if not intervals:
    #         raise ErrorDate(start_date, end_date, max_limit, occurrence, condition, include)
    #
    #     else:
    #         intervals = self.__convert_to_date(intervals).tolist()
    #
    #         if occurrence == 'left' or occurrence == 'right':
    #             occurrence_period = intervals[0] if occurrence == 'left' else intervals[-1]
    #
    #             start_date_interval = occurrence_period[0]
    #             end_date_interval = occurrence_period[-1]
    #             qty_days_current = self.__quantity_days(start_date_interval, end_date_interval)
    #
    #             if quantity_days <= qty_days_current:
    #                 if occurrence == 'left':
    #                     timestamp_start = occurrence_period[0]
    #                     timestamp_end = timestamp_start + (quantity_days - 1) * self.__step
    #                 else:
    #                     timestamp_end = occurrence_period[-1]
    #                     timestamp_start = timestamp_end - (quantity_days - 1) * self.__step
    #
    #                 return [timestamp_start, timestamp_end]
    #
    #             else:
    #                 raise ValueError(
    #                     f"Parameter 'quantity_days' should be less than or equal to {qty_days_current}. You have {quantity_days}.")
    #         else:
    #             raise ValueError(f"Your occurrence '{occurrence}' doesn't exist.")

    def get_values_on_interval(self, start_date, end_date):
        """Возвращает все значения хранения на интервале дат"""
        if self.comparing_dates(start_date, end_date):
            pass

        values = self.__cut_array(start_date, end_date, indexes=False)
        return values.tolist()

    def check_interval_limit(self, start_date, end_date, limit_value, condition='lower', include=True):
        """Проверка условия на интервале"""
        if self.comparing_dates(start_date, end_date):
            pass

        values = self.get_values_on_interval(start_date, end_date)
        current_value = max(values) if condition == 'lower' else min(values) if condition == 'higher' else None

        if isinstance(current_value, float):
            check = self.__set_sign_on_conditions(current_value, limit_value, condition=condition, include=include)
            return check
        else:
            raise ValueError(f"Your condition '{condition}' doesn't exist")
