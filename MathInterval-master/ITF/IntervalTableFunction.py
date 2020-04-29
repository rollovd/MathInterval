import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
sns.set()

class IntervalTableFunction:
    def __init__(self):
        self.discrete_points = np.array([], dtype='float64')
        self.points = np.array([], dtype='float64')

        self.__discrete_x_points = np.array([], dtype='float64')
        self.__getX = np.array([], dtype='float64')
        self.__oneX = set()
        self.__discreteX = set()

    def drawLineStorage(self, value_get=None, graph='all_intersections'):
        plt.figure(figsize=(15, 10))

        X_points = [x[0] for x in self.points]
        Y_points = [x[-1] for x in self.points]

        if value_get or value_get == 0:
            values = self.getArguments(value_get)

            if values:
                if len(values) > 1:
                    plt.plot(values, [value_get for _ in range(len(values))], color='r')
                else:
                    plt.plot([self.points[0][0], self.points[-1][0]], [value_get for _ in range(2)], color='r')

        plt.plot(X_points, Y_points)

    def drawLinesDiscrete(self):
        if self.discrete_points.size != 0:
            plt.figure(figsize=(15, 10))

            x = []
            y = []

            for pointline in self.discrete_points:
                arguments = [pointline[0] for _ in range(2)]
                values = pointline[1:].tolist()

                x += arguments
                y += values

            sns.pointplot(x, y, join=False)

    @staticmethod
    def __getCoordinates(point):
        x, y = point

        return x, y

    @staticmethod
    def __addValuesOut(row, add_interval):
        row[-1] += add_interval

        return row

    @staticmethod
    def __integrateTrapz(X_array, Y_array, range_):
        integrate = 0

        for i in range(range_):
            Y = [Y_array[i], Y_array[i + 1]]
            X = [X_array[i], X_array[i + 1]]

            integrate += np.trapz(y=Y, x=X)

        return integrate

    def __linearEquation(self, point1, point2, point_axis, axis='Y'):
        x1, y1 = self.__getCoordinates(point1)
        x2, y2 = self.__getCoordinates(point2)

        diff_x = x2 - x1
        diff_y = y2 - y1

        if axis == 'Y':
            find_axis = (point_axis - x1) * diff_y / diff_x + y1
        elif axis == 'X':
            find_axis = (point_axis - y1) * diff_x / diff_y + x1

        return find_axis

    def __comparingArguments(self, argument1, argument2):
        if argument1 == argument2:
            index1 = index2 = np.searchsorted(self.__getX, [argument1], side='left')[0]
            list_values = self.__allValuesArgument(index1, index2)
            return list_values

    def __assertArguments(self, argument1, argument2):
        if argument2 < argument1:
            return True

    def __rewriteArguments(self, argument1, argument2):
        if self.__assertArguments(argument1, argument2):
            return argument2, argument1
        else:
            return argument1, argument2

    #TODO Избавиться от if-else
    def __getMinMax(self, argumentStart, argumentEnd):
        length_array = len(self.__getX)

        index1 = np.searchsorted(self.__getX, argumentStart, side='left')
        index2 = np.searchsorted(self.__getX, argumentEnd, side='right')

        list_values = self.__allValuesArgument(index1, index2)

        if index1 == index2 == 0:
            list_values = [float(0)]

        elif index1 == index2 == length_array:
            list_values = [self.points[-1][-1]]
            # return [self.points[-1][-1]]

        elif index1 == 0:
            if index2 == length_array:
                pass

            else:
                arg_value = self.getValue(argumentEnd)
                list_values += [arg_value]

        elif index2 == length_array:
            arg_value = self.getValue(argumentStart)
            list_values += [arg_value]

        else:
            arg_value1 = self.getValue(argumentStart)
            arg_value2 = self.getValue(argumentEnd)
            list_values += [arg_value1, arg_value2]

        del length_array, index1, index2

        return list_values

    def __allValuesArgument(self, index1, index2):
        slice_list = self.points[index1:index2]
        list_values = [x[-1] for x in slice_list]

        return list_values

    def addInterval(self, argumentStart, argumentEnd, intervalValue):
        if self.__assertArguments(argumentStart, argumentEnd):
            raise AssertionError('ArgumentEnd must be more or equal ArgumentStart')

        point1 = [argumentStart, 0]
        point2 = [argumentEnd, intervalValue]

        if self.points.size == 0:
            self.points = np.array([point1, point2], dtype='float')
            self.__getX = np.array([argumentStart, argumentEnd], dtype='float64')

        else:
            binary_search = np.searchsorted(self.__getX, [argumentStart, argumentEnd], side='right').tolist()

            if argumentStart == argumentEnd and argumentStart in self.__oneX:
                index = binary_search[-1] - 1

                for i in range(index, self.points.shape[0]):
                    self.points[i][-1] += intervalValue

            else:
                if binary_search == [0, 0] or binary_search == [self.points.shape[0] for _ in range(2)]:
                    new_points = np.array([point1, point2])

                    if argumentEnd <= self.points[0][0]:
                        self.points = np.apply_along_axis(self.__addValuesOut, 1, self.points, intervalValue)

                    else:
                        increase_value = self.points[-1][-1]
                        new_points = np.apply_along_axis(self.__addValuesOut, 1, new_points, increase_value)
                else:
                    x1_index, x2_index = binary_search

                    Y_point1 = 0 if x1_index == 0 else self.__linearEquation(self.points[x1_index - 1],
                                                                             self.points[x1_index], point1[0])

                    Y_point2 = self.__linearEquation(self.points[x2_index - 1], self.points[x2_index], point2[0]) if \
                                    x2_index < self.points.shape[0] else self.points[-1][-1]

                    new_point_x1 = [argumentStart, Y_point1]
                    new_point_x2 = [argumentEnd, intervalValue + Y_point2]
                    new_points = np.array([new_point_x1, new_point_x2])

                    # self.points[x1_index: x2_index] += self.__linearEquation(point1, point2, self.points[i][0])
                    # self.points[x2_index: self.points.shape[0]] += intervalValue

                    for i in range(x1_index, self.points.shape[0]):
                        add_value = self.__linearEquation(point1, point2, self.points[i][0]) if i < x2_index else \
                                                                                                    intervalValue
                        self.points[i][-1] += add_value

                self.points = np.insert(self.points, binary_search, new_points, axis=0)
                self.__getX = np.insert(self.__getX, binary_search, [argumentStart, argumentEnd], axis=0)

        if argumentStart == argumentEnd:
            self.__oneX.add(argumentStart)

    def getValue(self, argument):
        index1 = np.searchsorted(self.__getX, argument, side='left')
        index2 = np.searchsorted(self.__getX, argument, side='right')

        list_values = self.__allValuesArgument(index1, index2)

        if list_values:
            value = list_values[-1]

        else:
            if index1 == 0:
                value = self.points[0][-1]

            elif index1 == len(self.points):
                value = self.points[-1][-1]

            else:
                point1 = self.points[index1 - 1]
                point2 = self.points[index1]
                value = self.__linearEquation(point1, point2, argument)

        return value

    @staticmethod
    def __checkValuesBetween(value1, value2, value_check):
        if value1 < value_check <= value2:
            return True
        elif value1 > value_check > value2:
            return True
        else:
            return False

    def getArguments(self, value):
        coords = self.points
        arguments = []

        for i in range(coords.shape[0] - 1):
            value1 = coords[i][-1]
            value2 = coords[i + 1][-1]

            if self.__checkValuesBetween(value1, value2, value):
                argument = self.__linearEquation(coords[i], coords[i + 1], value, axis='X')
                arguments.append(argument)

        arguments = sorted(list(set([round(x, 6) for x in arguments])))
        return arguments

    @staticmethod
    def __split_array(array, argumentStart, argumentEnd):
        index1, index2 = np.searchsorted(array, [argumentStart, argumentEnd], side='left')

        ready_array = [argumentStart] + array[index1: index2] + [argumentEnd]

        return sorted(list(set(ready_array)))

    def getLimitArguments(self, argumentStart, argumentEnd, maxLimit, draw_plot=False):
        argumentStart, argumentEnd = self.__rewriteArguments(argumentStart, argumentEnd)
        arguments = self.getArguments(maxLimit)

        all_possible_periods = self.__split_array(arguments, argumentStart, argumentEnd)

        periods = []
        for i in range(len(all_possible_periods) - 1):
            value1 = all_possible_periods[i]
            value2 = all_possible_periods[i + 1]

            value = self.getValue((value1 + value2) / 2)
            if value <= maxLimit:
                period = [value1, value2]
                periods.append(period)

        if draw_plot:
            plt.figure(figsize=(15, 10))

            X_points = [x[0] for x in self.points]
            Y_points = [x[-1] for x in self.points]

            X_rect = [argumentStart, argumentStart, argumentEnd, argumentEnd]
            Y_rect = [0, maxLimit, maxLimit, 0]

            plt.plot(X_points, Y_points)
            plt.plot(X_rect, Y_rect)

        if not periods:
            return [[]]
        else:
            return periods

    def getMaxBetween(self, argumentStart, argumentEnd):
        argumentStart, argumentEnd = self.__rewriteArguments(argumentStart, argumentEnd)

        comparing = self.__comparingArguments(argumentStart, argumentEnd)
        if comparing:
            max_value = max(comparing)

        else:
            list_values = self.__getMinMax(argumentStart, argumentEnd)
            max_value = max(list_values)

        return max_value

    def getMinBetween(self, argumentStart, argumentEnd):
        argumentStart, argumentEnd = self.__rewriteArguments(argumentStart, argumentEnd)

        comparing = self.__comparingArguments(argumentStart, argumentEnd)
        if comparing:
            min_value = min(comparing)

        else:
            list_values = self.__getMinMax(argumentStart, argumentEnd)
            min_value = min(list_values)

        return min_value

    #TODO Оптимизировать (особо не нужна)
    def getSumBetween(self, argumentStart, argumentEnd):
        argumentStart, argumentEnd = self.__rewriteArguments(argumentStart, argumentEnd)

        length_array = len(self.__getX)
        index1, index2 = np.searchsorted(self.__getX, [argumentStart, argumentEnd], side='left')

        list_values = self.__allValuesArgument(index1, index2)

        if index1 == index2 == 0:
            integrate = 0

        elif index1 == index2 == length_array:
            y_value = self.points[-1][-1]

            Y = [y_value for _ in range(2)]
            X = [argumentStart, argumentEnd]

            integrate = np.trapz(y=Y, x=X)

        elif index1 == 0:
            if index2 == length_array:
                y_value = self.points[-1][-1]
                x_value = self.__getX[-1]

                integrate = self.__integrateTrapz(self.__getX, list_values, length_array - 1)

                Y_extra = [y_value for _ in range(2)]

            else:
                X_line_interval = self.__getX[index1:index2]

                y_value = list_values[-1]
                x_value = X_line_interval[-1]
                value_argument = self.getValue(argumentEnd)

                integrate = self.__integrateTrapz(X_line_interval, list_values, len(list_values) - 1)

                Y_extra = [y_value, value_argument]

            X_extra = [x_value, argumentEnd]
            integrate += np.trapz(y=Y_extra, x=X_extra)

        elif index2 == length_array:
            X_line_interval = self.__getX[index1:index2]

            y_value_start = list_values[0]
            x_value_start = X_line_interval[0]
            value_argument = self.getValue(argumentStart)

            integrate = self.__integrateTrapz(X_line_interval, list_values, len(list_values) - 1)

            Y_start = [value_argument, y_value_start]
            X_start = [argumentStart, x_value_start]

            integrate1 = np.trapz(y=Y_start, x=X_start)

            y_value_end = list_values[-1]
            x_value_end = X_line_interval[-1]

            Y_end = [y_value_end for _ in range(2)]
            X_end = [x_value_end, argumentEnd]

            integrate2 = np.trapz(y=Y_end, x=X_end)

            integrate += integrate1 + integrate2

        else:
            X_line_interval = self.__getX[index1:index2]

            arg_value1 = self.getValue(argumentStart)
            arg_value2 = self.getValue(argumentEnd)

            if X_line_interval.size != 0:
                y_value_start = list_values[0]
                x_value_start = X_line_interval[0]

                y_value_end = list_values[-1]
                x_value_end = X_line_interval[-1]

                integrate = self.__integrateTrapz(X_line_interval, list_values, len(list_values) - 1)

                Y_start = [arg_value1, y_value_start]
                X_start = [argumentStart, x_value_start]

                integrate1 = np.trapz(y=Y_start, x=X_start)

                Y_end = [y_value_end, arg_value2]
                X_end = [x_value_end, argumentEnd]

                integrate2 = np.trapz(y=Y_end, x=X_end)

                integrate += integrate1 + integrate2

            else:
                Y_start = [arg_value1, arg_value2]
                X_start = [argumentStart, argumentEnd]

                integrate = np.trapz(y=Y_start, x=X_start)

        return integrate

    def __comparingMaxLimit(self, argument, maxLimit):
        y = self.getValue(argument)
        if maxLimit < y:
            return []
        else:
            return [argument]

    def addDiscreteInterval(self, argument, value):
        point_line = [argument, 0, value]

        if self.discrete_points.size == 0:
            self.discrete_points = np.array([point_line], dtype='float64')
            self.__discrete_x_points = np.array([argument], dtype='float64')
            self.__discreteX.add(argument)

        else:
            binary_search = np.searchsorted(self.__discrete_x_points, argument, side='left').tolist()
            if argument in self.__discreteX:
                self.discrete_points[binary_search][-1] += value

            else:
                self.discrete_points = np.insert(self.discrete_points, binary_search, point_line, axis=0)
                self.__discrete_x_points = np.insert(self.__discrete_x_points, binary_search, argument, axis=0)
                self.__discreteX.add(argument)

    def __getAllDiscreteArguments(self, value):
        arguments = [int(x[0]) for x in self.discrete_points if x[-1] > value]
        return arguments

    def __checkInArray(self, value, maxLimit):
        if value in self.__discreteX:
            value_index = np.squeeze(np.where(self.__discrete_x_points == value))
            value_point = self.discrete_points[value_index][-1]

            if maxLimit <= value_point:
                value -= 1
        else:
            pass

        return value

    def getDiscreteArguments(self, argumentStart, argumentEnd, maxLimit, timedelta_ = 86400):
        if self.__assertArguments(argumentStart, argumentEnd):
            raise AssertionError('ArgumentEnd must be more or equal ArgumentStart')

        all_arguments = self.__getAllDiscreteArguments(maxLimit)

        index1, index2 = np.searchsorted(all_arguments, [argumentStart, argumentEnd], side='left').tolist()
        result = all_arguments[index1:index2]

        if not result:
            argumentEnd = self.__checkInArray(argumentEnd, maxLimit)
            if argumentEnd >= argumentStart:
                total_gaps = [[argumentStart, argumentEnd]]
            else:
                total_gaps = [[]]

        else:
            total_gaps = []
            for_start = result[0]

            if len(result) == 1:
                if for_start != argumentStart:
                    first_interval = [argumentStart, for_start - timedelta_]
                    total_gaps.append(first_interval)

                for_end = for_start + timedelta_

            else:
                for_start -= timedelta_
                for_end = result[-1] + timedelta_

                for i in range(len(result) - 1):
                    first_value = result[i] + timedelta_
                    second_value = result[i + 1] - timedelta_

                    if first_value <= second_value:
                        check_interval = [first_value, second_value]
                        total_gaps.append(check_interval)

                if argumentStart <= for_start:
                    start_interval = [argumentStart, for_start]
                    total_gaps.insert(0, start_interval)

            argumentEnd = self.__checkInArray(argumentEnd, maxLimit)
            if argumentEnd >= for_end:
                second_interval = [for_end, argumentEnd]
                total_gaps.append(second_interval)

        if not total_gaps:
            total_gaps = [[]]

        try:
            to_float_vectorize = np.vectorize(lambda x: float(x))
            total_gaps = to_float_vectorize(total_gaps).tolist()
        except ValueError:
            pass

        return total_gaps

    @staticmethod
    def __from_timestamp(timestamp_value):
        get_date = datetime.datetime.fromtimestamp(timestamp_value).strftime('%Y/%m/%d')

        return get_date

    def discrete_timestamp_dates(self, array):
        if not array[0]:
            return [[]]
        else:
            timestamp_vectorize = np.vectorize(self.__from_timestamp)
            return timestamp_vectorize(array).tolist()
