import difflib
import os
import shutil
import subprocess
import sys
import time

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from threading import Thread

# slash = '/' # linux
slash = '\\'  # windows


class Data:
    def get_time(self, mask): return self.matrix_time[mask]

    def get_time_sum(self, mask): return np.sum(self.matrix_time[mask], axis=0)

    def get_tests_count(self): return len(self.matrix_time)

    def get_params(self): return self.params

    def get_results_tests(self, mask): return self.matrix_is_complete[mask]

    def get_test_name(self, mask): return self.test_name[mask]

    def clear_data(self):
        self.matrix_time.clear()
        self.matrix_is_complete.clear()

    def download_data(self):
        file = open(self.path_statistic, 'r')
        b, g = file.readline()
        # finish writing

    def __init__(self, matrix_time, matrix_is_complete, path_statistic, test_name, params):
        super().__init__()
        self.matrix_time = matrix_time
        self.matrix_is_complete = matrix_is_complete
        self.path_statistic = path_statistic
        self.test_name = test_name
        self.params = params


class Kernel:

    @staticmethod
    def __is_equal_file_default(path1, path2):
        if not os.path.isfile(path1) or not os.path.isfile(path1):
            return False
        file1 = open(path1, 'r')  # result
        file2 = open(path2, 'r')  # reference
        diff = difflib.ndiff(file1.readlines(), file2.readlines())
        return ''.join(x for x in diff if x.startswith('- ')) == ""

    @staticmethod
    def __is_equal_file_true(path1, path2):
        return True

    @staticmethod
    def __is_equal_file_user(path):
        def func(path1, path2):
            if not os.path.isfile(path1) or not os.path.isfile(path1):
                return False
            return subprocess.check_output([path, path1, path2]).__str__() == 'b\'1\''

        return func

    def __init__(self):
        self.__program = ""
        self.__output = ""
        self.params = np.array([int(1), int(1)])
        self.__matrix_time = np.array([])
        self.__matrix_is_complete = np.array([])
        self.__cmp = self.__is_equal_file_default

    def __execute_test(self, test, res_i, reference, stat):
        time_work = -1 * np.ones(int(self.params[1] + 1 - self.params[0]))
        is_complete = np.array([False for i in range(self.params[1] + 1 - self.params[0])])
        for i in range(int(self.params[1] + 1 - self.params[0])):
            param = (i + self.params[0]).__str__()
            res = res_i + slash + param + ".txt"
            timer = time.time()
            # print(timer)
            # subprocess.check_call([__program, param, test, res]) with exception
            # subprocess.call([self.__program, param, test, res])  # without exception
            qqq = subprocess.check_output([self.__program, param, test, res]).__str__()
            # print(time.time())
            time_work[i] = time.time() - timer
            is_complete[i] = self.__cmp(res, reference)
            stat.write(test + '; ' + param + '; ' + (time_work[i]).__str__() + '; ' + (is_complete[i]).__str__() + '\n')
        return [time_work, is_complete]

    def __execute_test_wo_ref(self, test, stat):  # without output
        time_work = -1 * np.ones(int(self.params[1] + 1 - self.params[0]))
        for i in range(int(self.params[1] + 1 - self.params[0])):
            param = (i + self.params[0]).__str__()
            timer = time.time()
            qqq = subprocess.check_output([self.__program, param, test]).__str__()
            time_work[i] = time.time() - timer
            stat.write(test + '; ' + param + '; ' + (time_work[i]).__str__() + '\n')
        return time_work

    def __start_tests(self, path_test, tests, path_reference, references):
        self.__matrix_time = np.array([np.zeros(self.params[1] + 1 - self.params[0])])
        self.__matrix_is_complete = np.array([[False for i in range(self.params[1] + 1 - self.params[0])]])
        stat = open(self.__output + "statistic.csv", 'w')
        # stat.write(self.params.__str__() + "\n")
        stat.write("test_name; param; time; result\n")
        for i in range(len(tests)):
            test = path_test + tests[i]
            reference = path_reference + references[i]
            res = self.__output + i.__str__()
            os.mkdir(res)
            a, b = self.__execute_test(test, res, reference, stat)
            self.__matrix_time = np.append(self.__matrix_time, [a], axis=0)
            self.__matrix_is_complete = np.append(self.__matrix_is_complete, [b], axis=0)
            # stat.write(tests[i] + "\n")
            # stat.write("time: " + self.__matrix_time[i + 1].__str__() + "\n")
            # stat.write("result: " + self.__matrix_is_complete[i + 1].__str__() + "\n")
        self.__matrix_time = np.delete(self.__matrix_time, 0, axis=0)
        self.__matrix_is_complete = np.delete(self.__matrix_is_complete, 0, axis=0)
        # stat.write("all time: " + np.sum(self.__matrix_time, axis=0).__str__())
        stat.close()

    def __start_tests_wo_ref(self, path_test, tests):
        self.__matrix_time = np.array([np.zeros(self.params[1] + 1 - self.params[0])])
        stat = open(self.__output + "statistic.csv", 'w')
        stat.write("test_name; param; time\n")
        for i in range(len(tests)):
            test = path_test + tests[i]
            self.__matrix_time = np.append(self.__matrix_time, [self.__execute_test_wo_ref(test, stat)], axis=0)
        self.__matrix_time = np.delete(self.__matrix_time, 0, axis=0)
        stat.close()

    def __validation(self, path_test, path_reference, path_cmp):
        is_valid = True
        message = ""

        t = os.path.isfile(self.__program)
        if not t:
            message += "path program\n"
        is_valid &= t

        t = os.path.exists(path_test)
        count_test = 0
        if not t:
            message += "path test\n"
        else:
            count_test = 1
            if os.path.isdir(path_test):
                listdir = os.listdir(path_test)
                count_test = len(listdir)
                for file_name in listdir:
                    if os.path.isdir(path_test + slash + file_name):
                        t = False
                        message += 'test include dir\n'
                        break
        is_valid &= t

        if not os.path.isdir(self.__output):
            self.__output = os.getcwd()
            message += "path result\n"

        count_reference = 0
        t = path_reference == "" or os.path.exists(path_reference)
        if not t:
            message += "path reference\n"
        else:
            count_reference = 1
            if os.path.isdir(path_reference):
                listdir = os.listdir(path_reference)
                count_reference = len(listdir)
                for file_name in listdir:
                    if os.path.isdir(path_reference + slash + file_name):
                        t = False
                        message += 'reference include dir\n'
                        break
        is_valid &= t

        t = count_reference == count_test
        if is_valid and not t:
            message += 'quantity mismatch reference, test\n'
        is_valid &= t

        if os.path.isfile(path_cmp):
            self.__cmp = self.__is_equal_file_user(path_cmp)
        else:
            message += "path comparator\n"
        return is_valid, message

    def start_test_by_path(self, path_exe, path_test, params, path_res, path_reference, path_cmp, interpolation_string):
        self.__program = path_exe
        self.params = [min(params), max(params)]    
        self.__output = path_res
        is_valid, message = self.__validation(path_test, path_reference, path_cmp)
        if not is_valid:
            return None, message
        self.__output += slash + 'results'
        if os.path.isdir(self.__output):
            shutil.rmtree(self.__output)

        tests = np.array([""])
        if os.path.isdir(path_test):  # check path_test is fold or file
            tests = np.array(os.listdir(path_test))
            path_test += slash

        if path_reference == "":
            os.mkdir(self.__output)
            self.__output += slash
            self.__start_tests_wo_ref(path_test, tests)
            return Data(self.__matrix_time, self.__matrix_is_complete, path_test + "statistic.txt", tests,
                        self.params), message

        reference = np.array([""])
        if os.path.isdir(path_reference):  # check path_reference is    fold or file
            reference = np.array(os.listdir(path_reference))
            path_reference += slash

        os.mkdir(self.__output)
        self.__output += slash
        self.__start_tests(path_test, tests, path_reference, reference)
        return Data(self.__matrix_time, self.__matrix_is_complete, path_test + "statistic.txt", tests,
                    self.params), message


# Next code is UI


class ProgressWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.main_vertical_layout = QVBoxLayout()
        self.progress_bar = QProgressBar(self)
        self.progress_label = QLabel("РЎРґРµР»Р°РЅРѕ СЃС‚РѕР»СЊРєРѕ С‚Рѕ С‚РµСЃС‚РѕРІ")
        self.main_vertical_layout.addWidget(self.progress_label)
        self.main_vertical_layout.addWidget(self.progress_bar)
        self.setLayout(self.main_vertical_layout)
        self.setWindowTitle("Progress:")
        self.setGeometry(400, 400, 300, 70)

    def set_test_status(self, complete, number_of_test):
        self.progress_bar.setValue(complete * 100 / number_of_test)
        self.progress_label.setText(f"Complete {complete} tests of {number_of_test}")

    def get_test_setter(self):
        return self.set_test_status


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.error_window = ErrorWindow()
        self.kernel = Kernel()
        self.data = []
        self.mask = []
        self.progressive_window = ProgressWindow()
        self.result = None
        main_horizontal_layout = QHBoxLayout()

        main_vertical_layout = QVBoxLayout()

        test_scenario_label = QLabel("Path to executable scenario file")
        self.test_scenario_path = QLineEdit()

        path_tests_label = QLabel("Path to file(folder) with the test(tests)")
        self.path_tests_path = QLineEdit()

        test_params_layout = QHBoxLayout()
        test_params_layout.addStretch(0)
        self.test_params_label = QLabel("Current Param Range (min = 1, max = 1000)")
        self.test_params_value_min = QLineEdit("1")
        self.test_params_value_min.textChanged.connect(self.on_value_changed_min)
        self.test_params_value_max = QLineEdit("1000")
        self.test_params_value_max.textChanged.connect(self.on_value_changed_max)
        test_params_layout.addWidget(self.test_params_label)
        test_params_layout.addWidget(self.test_params_value_min)
        test_params_layout.addStretch(0)
        test_params_layout.addWidget(self.test_params_value_max)
        test_params_layout.addStretch(20)

        path_answers_label = QLabel("Path to folder with default test results")
        self.path_answers_path = QLineEdit()

        path_result_label = QLabel("Path to folder to save the results")
        self.path_result_path = QLineEdit()

        path_comp_label = QLabel("Path to answers comparator executable file")
        self.path_comp_path = QLineEdit()

        calc_button = QPushButton("Start Testing")
        calc_button.clicked.connect(self.on_calc_click)

        self.param_line_edit = QLineEdit()
        self.param_line_edit_label = QLabel("Interpolation string")

        main_vertical_layout.addStretch(1)
        main_vertical_layout.addWidget(test_scenario_label)
        main_vertical_layout.addStretch(0)
        main_vertical_layout.addWidget(self.test_scenario_path)
        main_vertical_layout.addStretch(1)
        main_vertical_layout.addWidget(path_tests_label)
        main_vertical_layout.addStretch(0)
        main_vertical_layout.addWidget(self.path_tests_path)
        main_vertical_layout.addStretch(1)
        main_vertical_layout.addLayout(test_params_layout)
        main_vertical_layout.addStretch(1)
        main_vertical_layout.addWidget(path_answers_label)
        main_vertical_layout.addStretch(0)
        main_vertical_layout.addWidget(self.path_answers_path)
        main_vertical_layout.addStretch(1)
        main_vertical_layout.addWidget(path_result_label)
        main_vertical_layout.addStretch(0)
        main_vertical_layout.addWidget(self.path_result_path)
        main_vertical_layout.addStretch(1)
        main_vertical_layout.addWidget(path_comp_label)
        main_vertical_layout.addStretch(0)
        main_vertical_layout.addWidget(self.path_comp_path)
        main_vertical_layout.addStretch(1)
        main_vertical_layout.addWidget(self.param_line_edit_label)
        main_vertical_layout.addStretch(0)
        main_vertical_layout.addWidget(self.param_line_edit)
        main_vertical_layout.addStretch(1)
        main_vertical_layout.addWidget(calc_button)

        main_horizontal_layout.addLayout(main_vertical_layout)

        self.setLayout(main_horizontal_layout)
        self.setGeometry(300, 200, 1280, 720)
        self.showFullScreen()
        self.setWindowTitle('QLineEdit')

    def on_value_changed_min(self):
        if len(self.test_params_value_min.text()) != 0:
            try:
                temp_value = int(self.test_params_value_min.text())
            except ValueError:
                temp_value = 1
            if temp_value > 1000 or temp_value < 1:
                temp_value = 0
            self.test_params_value_min.setText(str(temp_value))

    def on_value_changed_max(self):
        if len(self.test_params_value_max.text()) != 0:
            try:
                temp_value = int(self.test_params_value_max.text())
            except ValueError:
                temp_value = 1000
            if temp_value > 1000 or temp_value < 1:
                temp_value = 1000
            self.test_params_value_max.setText(str(temp_value))

    def on_calc_click(self):
        path_exe = self.test_scenario_path.text()
        path_test = self.path_tests_path.text()
        # params =  [2, 4]
        params = [int(self.test_params_value_min.text()), int(self.test_params_value_max.text())]

        path_reference = self.path_answers_path.text()
        path_res = self.path_result_path.text()
        cmp = self.path_comp_path.text()
        d = data_for_test()
        interpolation_string = self.param_line_edit.text()
        # result, message = self.kernel.start_test_by_path(path_exe, path_test, params, path_res, path_reference, cmp,
        #                                                 self.progressive_window.get_test_setter())

        result, message = self.kernel.start_test_by_path(d[0], d[1], d[2], d[3], d[4], d[5], interpolation_string)

        if result is None:
            self.error_window.set_title("Error!")
            self.error_window.set_error(message)
            self.error_window.show()
        else:
            print(result.get_time([True for i in range(result.get_tests_count())]))
            self.mask = [True for i in range(result.get_tests_count())]
            test_info = get_configuration_list(result, self.mask)
            self.result = ResultWindow(test_info)
            self.result.show()

            if len(message) != 0:
                self.error_window.set_title("Warning!")
                self.error_window.set_error(f"{message}We used default")
                self.error_window.show()


class ResultWindow(QWidget):
    def template(self, number, func):
        def f():
            return self.on_curve_show_change(number, func())

        return f

    def __init__(self, result_data):
        super().__init__()
        self.setGeometry(300, 200, 1280, 720)
        self.result_list = QVBoxLayout()
        for i in range(len(result_data)):
            self.result_list.addLayout(
                self.get_result_item(result_data[i], i)
            )
            self.result_list.addSpacing(35)

        self.result = result_data

        group_box = QGroupBox()
        group_box.setLayout(self.result_list)
        self.scroll = QScrollArea()
        self.scroll.setWidget(group_box)
        self.scroll.setWidgetResizable(True)

        self.left_vertical_layout = QVBoxLayout()
        self.left_vertical_layout.addWidget(self.scroll)
        self.sum_check_box = QCheckBox("Display result Sum")
        self.sum_check_box.stateChanged.connect(self.on_sum_show_change)
        self.left_vertical_layout.addWidget(self.sum_check_box)

        self.curve_status_show = [True for i in range(len(result_data))]

        self.test_names = [test[0].name for test in result_data]

        self.result_graph = PlotCanvas(width=8, height=8, curve_status_show=self.curve_status_show, data=result_data,
                                       test_names=self.test_names)
        self.main_horizontal_layout = QHBoxLayout()
        self.main_horizontal_layout.setAlignment(Qt.AlignRight)
        self.main_horizontal_layout.addLayout(self.left_vertical_layout)
        self.main_horizontal_layout.addWidget(self.result_graph)
        self.main_horizontal_layout.setAlignment(Qt.AlignLeft)

        self.setLayout(self.main_horizontal_layout)

    def on_sum_show_change(self):
        if not (not self.sum_check_box.checkState() == Qt.Checked):
            self.main_horizontal_layout.removeWidget(self.result_graph)
            self.result_graph.resize(0, 0)
            self.result_graph = PlotCanvasSum(width=8, height=8, curve_status_show=self.curve_status_show,
                                              data=self.result,
                                              test_names=self.test_names)
            self.main_horizontal_layout.addWidget(self.result_graph)
        else:
            self.main_horizontal_layout.removeWidget(self.result_graph)
            self.result_graph.resize(0, 0)
            self.result_graph = PlotCanvas(width=8, height=8, curve_status_show=self.curve_status_show, data=self.result,
                                       test_names=self.test_names)
            self.main_horizontal_layout.addWidget(self.result_graph)

    def on_curve_show_change(self, number_of_curve, status):
        self.sum_check_box.setChecked(False)
        self.curve_status_show[number_of_curve] = status
        self.main_horizontal_layout.removeWidget(self.result_graph)
        self.result_graph.resize(0, 0)
        self.result_graph = PlotCanvas(width=8, height=8, curve_status_show=self.curve_status_show, data=self.result,
                                       test_names=self.test_names)
        self.main_horizontal_layout.addWidget(self.result_graph)

    def get_result_item(self, data_list, number_of_test):
        item_layout = QHBoxLayout()
        item_check_box = QCheckBox()
        left_vertical_layout = QVBoxLayout()
        item_check_box.setChecked(True)
        item_check_box.stateChanged.connect(
            self.template(number_of_test, item_check_box.isChecked))
        left_vertical_layout.addWidget(item_check_box)
        left_vertical_layout.addStretch(1)
        item_layout.addLayout(left_vertical_layout)
        item_layout.addStretch(0)
        sub_items_layout = QVBoxLayout()
        for data in data_list:
            sub_record_layout = QHBoxLayout()
            item_name = QLabel(f"Test name: {data.name}", )
            item_time = QLabel(f"Execution time: {round(data.time, 6)} seconds,")
            item_status = QLabel(f"Test status: {data.status},")
            item_number = QLabel(str(data.number) + ",")
            item_number_cores = QLabel(f"Param value: {data.param_value}")

            sub_record_layout.addWidget(item_name)
            sub_record_layout.addWidget(item_time)
            sub_record_layout.addWidget(item_status)
            sub_record_layout.addWidget(item_number)
            sub_record_layout.addWidget(item_number_cores)

            sub_items_layout.addLayout(sub_record_layout)
        # sub_items_layout.addStretch(0.1) maybe do something with space between items
        item_layout.addLayout(sub_items_layout)
        item_layout.addStretch(0)
        return item_layout


class PlotCanvasSum(FigureCanvas):
    def __init__(self, width=7, height=7, dpi=80, data=None, curve_status_show=None, test_names=[]):
        if curve_status_show is None:
            curve_status_show = []
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)

        self.plot(data, curve_status_show)
        self.draw()

    def plot(self, data_list, curve_status_show):
        ax = self.figure.add_subplot(111)
        sum_y = np.zeros_like(data_list[0])
        x = np.array([current_test.param_value for current_test in data_list[-1]])
        for test in range(len(data_list)):
            if curve_status_show[test]:
                y = np.array([current_test.time for current_test in data_list[test]])
                sum_y += y
        ax.plot(x, sum_y, label="Test: Result sum")
        ax.scatter(x=x, y=sum_y, color="red")

        ax.legend()
        ax.set_ylabel("Execution time")
        ax.set_xlabel("Param value")
        ax.grid()
        ax.set_title("Tasks Graph")


class PlotCanvas(FigureCanvas):

    def __init__(self, width=7, height=7, dpi=80, data=None, curve_status_show=None, test_names=[]):
        if curve_status_show is None:
            curve_status_show = []
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)

        self.plot(data, curve_status_show, test_names)
        self.draw()

    def plot(self, data_list, curve_status_show, test_names):
        ax = self.figure.add_subplot(111)
        for test in range(len(data_list)):
            if curve_status_show[test]:
                x = np.array([current_test.param_value for current_test in data_list[test]])
                y = np.array([current_test.time for current_test in data_list[test]])
                ax.plot(x, y, label=f"Test: {test_names[test]}")
                for config in range(len(data_list[test])):
                    if data_list[test][config].status == "Complete":
                        ax.scatter(x=data_list[test][config].param_value, y=data_list[test][config].time, color="green")
                    else:
                        ax.scatter(x=data_list[test][config].param_value, y=data_list[test][config].time, color="red")

        ax.legend()
        ax.set_ylabel("Execution time")
        ax.set_xlabel("Param value")
        ax.grid()
        ax.set_title("Tasks Graph")


class ErrorWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Next data is not valid!"))
        self.error_text = QLabel("")
        layout.addWidget(self.error_text)
        self.setLayout(layout)
        self.setGeometry(600, 500, 300, 100)
        self.setWindowTitle("Error!")

    def set_error(self, error_text):
        self.error_text.setText(error_text)

    def set_title(self, title):
        self.setWindowTitle(title)


class TestConfiguration:
    def __init__(self, name, time_stat, status, number, count_of_cores):
        self.name = name
        self.time = time_stat
        self.status = status
        self.number = number
        self.param_value = count_of_cores


def get_configuration_list(data_list, mask):
    params = data_list.get_params()
    delta = params[1] - params[0] + 1

    configuration_time_list = data_list.get_time(mask)
    configuration_status_list = data_list.get_results_tests(mask)
    configuration_name_list = data_list.get_test_name(mask)

    return np.array([[TestConfiguration(
        configuration_name_list[j],  # test_name should be here
        configuration_time_list[j][i],
        "Complete" if (configuration_status_list[j][i]) else "Failed",
        delta * j + i,
        params[0] + i)
        for i in range(delta)] for j in range(len(configuration_time_list))])


import unittest


def data_for_test():
    this_path = os.getcwd()
    return [this_path + slash + 'test' + slash + 'main.exe',  # 0
            this_path + slash + 'test' + slash + 'test',  # 1
            [1, 4],  # 2
            this_path + slash + 'test',  # 3
            this_path + slash + 'test' + slash + 'reference',  # 4
            this_path + slash + 'test' + slash + 'cmp.exe']  # 5


class TestKernel(unittest.TestCase):
    kernel = Kernel()
    d = data_for_test()
    app = QApplication(sys.argv)
    error_window = ErrorWindow()
    error_window.set_title("Error!")
    error_window.set_error("Some errors!")

    # corrects

    def test_error_window_title(self):
        self.assertEqual("Error!", self.error_window.windowTitle())

    def test_error_window_content(self):
        self.assertEqual("Some errors!", self.error_window.error_text.text())

    def test_correct_1(self):
        res, message = self.kernel.start_test_by_path(self.d[0], self.d[1], self.d[2], self.d[3], self.d[4], self.d[5])
        self.assertTrue(res is not None)
        self.assertEqual(message, "")

    def test_correct_2(self):
        res, message = self.kernel.start_test_by_path(self.d[0], self.d[1] + slash + 'test1.txt', self.d[2],
                                                      self.d[3], self.d[4] + slash + 'res2.txt', self.d[5])
        self.assertTrue(res is not None)
        self.assertEqual(message, "")

    def test_correct_3(self):
        res, message = self.kernel.start_test_by_path(self.d[0], self.d[1] + '2', self.d[2],
                                                      self.d[3], self.d[4] + slash + 'res1.txt', self.d[5])
        self.assertTrue(res is not None)
        self.assertEqual(message, "")

    # errors

    def test_program_not_correct(self):
        res, message = self.kernel.start_test_by_path('c:\\mIN.exe', self.d[1], self.d[2],
                                                      self.d[3], self.d[4], self.d[5])
        self.assertTrue(res is None)
        self.assertEqual(message, 'path program\n')

    def test_not_correct(self):
        res, message = self.kernel.start_test_by_path(self.d[0], 'c:\\main', self.d[2],
                                                      self.d[3], self.d[4], self.d[5])
        self.assertTrue(res is None)
        self.assertEqual(message, 'path test\n')

    def test_include_dir(self):
        os.mkdir(self.d[1] + '\\temp')
        res, message = self.kernel.start_test_by_path(self.d[0], self.d[1], self.d[2],
                                                      self.d[3], self.d[4], self.d[5])
        self.assertTrue(res is None)
        self.assertEqual(message, "test include dir\n")
        os.rmdir(self.d[1] + '\\temp')

    def test_and_program_not_correct(self):
        res, message = self.kernel.start_test_by_path('c:\\mIN.exe', 'c:\\main', self.d[2],
                                                      self.d[3], self.d[4], self.d[5])
        self.assertTrue(res is None)
        self.assertEqual(message, 'path program\npath test\n')

    def test_reference_not_correct(self):
        res, message = self.kernel.start_test_by_path(self.d[0], self.d[1], self.d[2],
                                                      self.d[3], 'file_name', self.d[5])
        self.assertTrue(res is None)
        self.assertEqual(message, 'path reference\n')

    def test_reference_include_dir(self):
        os.mkdir(self.d[4] + slash + 'temp')
        res, message = self.kernel.start_test_by_path(self.d[0], self.d[1], self.d[2],
                                                      self.d[3], self.d[4], self.d[5])
        self.assertTrue(res is None)
        self.assertEqual(message, 'reference include dir\n')
        os.rmdir(self.d[4] + slash + 'temp')

    def test_mismatch_test_reference_1(self):
        res, message = self.kernel.start_test_by_path(self.d[0], self.d[1], self.d[2],
                                                      self.d[3], self.d[4] + slash + 'res1.txt', self.d[5])
        self.assertTrue(res is None)
        self.assertEqual(message, 'quantity mismatch reference, test\n')

    def test_mismatch_test_reference_2(self):
        res, message = self.kernel.start_test_by_path(self.d[0], self.d[1] + slash + 'test1.txt', self.d[2],
                                                      self.d[3], self.d[4], self.d[5])
        self.assertTrue(res is None)
        self.assertEqual(message, 'quantity mismatch reference, test\n')

    # warnings

    def test_result_not_correct(self):
        res, message = self.kernel.start_test_by_path(self.d[0], self.d[1], self.d[2],
                                                      'file_name', self.d[4], self.d[5])
        self.assertTrue(res is not None)
        self.assertEqual(message, 'path result\n')

    def test_cmp_not_correct(self):
        res, message = self.kernel.start_test_by_path(self.d[0], self.d[1], self.d[2],
                                                      self.d[3], self.d[4], self.d[4])
        self.assertTrue(res is not None)
        self.assertEqual(message, 'path comparator\n')


if __name__ == "__main__":
    # unittest.main()
    app = QApplication(sys.argv)
    print("5, 9")
    # time.sleep(10)
    ex = MainWindow()
    ex.on_calc_click()
    ex.show()
    # ex.set_test_status(1, 9)
    sys.exit(app.exec_())
    # ex = ProgressWindow()
