import datetime

class NoHandlingPowerException(Exception):
    def __init__(self, name, load_type, end_date):
        self.name = name
        self.load_type = load_type
        self.end_date = end_date

class IncorrectIntervalError(Exception):
    def __init__(self, start_date, end_date):
        self.start_date = self.from_timestamp(start_date)
        self.end_date = self.from_timestamp(end_date)

    @staticmethod
    def from_timestamp(timestamp_value):
        """Конвертирует timestamp в datetime.datetime формата YYYY/MM/DD"""
        get_date = datetime.datetime.fromtimestamp(timestamp_value).strftime('%Y/%m/%d')
        return get_date

    def __str__(self):
        return f"{self.start_date} should be less or equal than {self.end_date}"

class LimitError(Exception):
    def __init__(self, min_possible_value, max_possible_value, value):
        self.min_possible_value = min_possible_value
        self.max_possible_value = max_possible_value
        self.value = value

    def __str__(self):
        current_min = self.min_possible_value
        current_max = self.max_possible_value
        return f"Your value {self.value} must be in the range {current_min} to {current_max} (not inclusive)"

class ErrorDate(Exception):
    def __init__(self, start_date, end_date, max_limit, occurrence, condition, include):
        self.start_date = start_date.strftime('%Y/%m/%d')
        self.end_date = end_date.strftime('%Y/%m/%d')
        self.max_limit = max_limit
        self.occurrence = occurrence
        self.condition = condition
        self.include = include

    def __str__(self):
        max_limit = f'max_limit: {self.max_limit}'
        occurrence = f'occurrence: {self.occurrence}'
        condition = f'condition: {self.condition}'
        include = f'include: {self.include}'

        parameters = f'{max_limit}, {occurrence}, {condition}, {include}'
        return f"Any required date on interval {self.start_date} - {self.end_date} doesn't exist.\nParameters: {parameters}"

class ComparingError(Exception):
    def __init__(self, start_date, end_date):
        self.start_date = start_date.strftime('%Y/%m/%d')
        self.end_date = end_date.strftime('%Y/%m/%d')

    def __str__(self):
        return f"end date should be more or equal than start date.\nYou have: start_date = {self.start_date}, end_date = {self.end_date}"

class OutTimestamp(Exception):
    def __init__(self, timestamp_error, timestamp1, timestamp2):
        self.date = self.from_timestamp(timestamp_error)
        self.date1 = self.from_timestamp(timestamp1)
        self.date2 = self.from_timestamp(timestamp2)

    @staticmethod
    def from_timestamp(timestamp_value):
        get_date = datetime.datetime.fromtimestamp(timestamp_value).strftime('%Y/%m/%d')
        return get_date

    def __str__(self):
        return f"{self.date} is out of range on the period {self.date1}-{self.date2}"
