from ITF.DiscreteIntervalTableFunction import DiscreteIntervalTableFunction
from Elements.exceptions import LimitError

class DiscreteIntervalTableFunctionLimit(DiscreteIntervalTableFunction):
    def __init__(self, start_date, end_date, max_possible_value, min_possible_value):
        DiscreteIntervalTableFunction.__init__(self, start_date, end_date)
        self.max_possible_value = max_possible_value
        self.min_possible_value = min_possible_value

    def __check_limit(self, value):
        """Входит ли новое значение в установленные пределы"""
        result = True if self.min_possible_value < value < self.max_possible_value else False
        return result

    def add_date(self, date, value):
        """Добавление значения хранения для заданной даты"""
        if self.__check_limit(value):
            super(DiscreteIntervalTableFunctionLimit, self).add_date(date, value)
        else:
            raise LimitError(self.min_possible_value, self.max_possible_value, value)

    def add_interval(self, date, value):
        """Добавление значения хранения для интервала дат"""
        if self.__check_limit(value):
            super(DiscreteIntervalTableFunctionLimit, self).add_interval(date, value)
        else:
            raise LimitError(self.min_possible_value, self.max_possible_value, value)