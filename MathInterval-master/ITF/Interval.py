import datetime
from Elements.exceptions import IncorrectIntervalError

class Interval:
    def __init__(self, start_date, end_date):
        self.__start_date = self.__check_type_of_date(start_date)
        self.__end_date = self.__check_type_of_date(end_date)

    def __check_type_of_date(self, date):
        """Проверка корректности входных данных"""
        if isinstance(date, float):
            return date
        else:
            return self.convert_to_timestamp(date)

    @staticmethod
    def convert_to_timestamp(date):
        """Конвертирует дату формата datetime.datetime в timestamp"""
        return date.timestamp()

    @staticmethod
    def from_timestamp(timestamp_value):
        """Конвертирует timestamp в datetime.datetime формата YYYY/MM/DD"""
        get_date = datetime.datetime.fromtimestamp(timestamp_value).strftime('%Y/%m/%d')
        return get_date

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, date):
        current_date = self.__check_type_of_date(date)

        if current_date <= self.__end_date:
            self.__start_date = current_date
        else:
            start_date_exception = self.from_timestamp(current_date)
            end_date_exception = self.from_timestamp(self.__end_date)
            raise IncorrectIntervalError(start_date_exception, end_date_exception)

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, date):
        current_date = self.__check_type_of_date(date)

        if current_date >= self.__start_date:
            self.__end_date = current_date
        else:
            start_date_exception = self.from_timestamp(self.__start_date)
            end_date_exception = self.from_timestamp(current_date)
            raise IncorrectIntervalError(start_date_exception, end_date_exception)

