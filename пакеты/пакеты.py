import difflib
import os
import random
import subprocess
import time
import sys

path = "C:\Users\Евгений\Desktop\Программы\AM-MP.2semestr\QA_practic\пакеты\test"
test = os.listdir(path)

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import shutil
import json


class Data:
    __matrix_time = None
    __matrix_is_complete = None
    __path_statistic = None

    def get_time(self, mask): return np.sum(self.__matrix_time[mask], axis=0)

    def get_time_tests(self, index): return self.__matrix_time[index]

    def get_results_tests(self, index): return self.__matrix_is_complete[index]

    def clear_data():
        __matrix_time.clear()
        __matrix_is_complete.clear()

    def download_data():
        file = open(self.__path_statistic, 'r')
        b, g = file.readline()
        # finish writing

    def __init__(self, matrix_time, matrix_is_complete, path_statistic):
        super().__init__()
        __matrix_time = matrix_time
        __matrix_is_complete = matrix_is_complete
        __path_statistic = path_statistic


class Kernel:
    __program = ""
    __output = ""
    __params = [0, 0]
    __matrix_time = np.array([])
    __matrix_is_complete = np.array([])

    @staticmethod
    def __is_equal_file_default(path1, path2):
        file1 = open(path1, 'r')  # tyt nado ykazuvat to chto nakhoditsa pod somneniem
        file2 = open(path2, 'r')  # tyt etalon
        diff = difflib.ndiff(file1.readlines(), file2.readlines())
        return ''.join(x for x in diff if x.startswith('- ')) == ""

    @staticmethod
    def __is_equal_file_true(path1, path2):
        return True

    @staticmethod
    def __is_equal_file_user(path):
        def func(path1, path2):
            return subprocess.check_output([path, path1, path2])

        return func

    __cmp = __is_equal_file_default

    def __execute_test(self, test, res_i, reference):
        time_work = -1 * np.ones(self.__params[1] + 1 - self.__params[0])
        is_complete = np.array([False] * (self.__params[1] + 1 - self.__params[0]))
        for i in range(0, self.__params[1] + 1 - self.__params[0]):
            param = (i + self.__params[0]).__str__()
            res = res_i + "\\" + param + ".txt"
            timer = time.clock()
            # subprocess.check_call([__program, param, test, res]) with exception
            subprocess.call([self.__program, param, test, res])  # without exception
            time_work[i] = time.clock() - timer
            is_complete[i] = self.__cmp(res, reference)
        return time_work, is_complete

    def __execute_test(self, test):  # without output
        time_work = -1 * np.ones(self.__params[1] + 1 - self.__params[0])
        for i in range(0, self.__params[1] + 1 - self.__params[0]):
            timer = time.clock()
            subprocess.call([self.__program, (i + self.__params[0]).__str__(), test])
            time_work[i] = time.clock() - timer
        return time_work

    def __start_tests(self, path_test, tests, path_reference, references):
        self.__matrix_time = np.array(len(tests))
        self.__matrix_is_complete = np.array(len(tests))
        stat = open(path_res + "statistic.txt", 'w')
        stat.write(self.__params.__str__() + "\n")
        for i in range(0, len(tests)):
            test = path_test + tests[i]
            reference = path_reference + references[i]
            res = path_res + i.__str__()
            os.mkdir(res)
            self.__matrix_time[i], self.__matrix_is_complete[i] = self.__execute_test(test, res, reference)
            stat.write(tests[i] + "\n")
            stat.write("time: " + self.__matrix_time[i].__str__() + "\n")
            stat.write("result: " + self.__matrix_is_complete[i].__str__() + "\n")
        stat.write("all time: " + np.sum(self.__matrix_time, axis=0).__str__())
        stat.close()

    def __start_tests(self, path_test, tests):
        self.__matrix_time = np.array(len(tests))
        stat = open(self.__output + "statistic.txt", 'w')
        for i in range(0, len(tests)):
            test = path_test + tests[i]
            self.__matrix_time[i] = self.__execute_test(test)
            stat.write(tests[i] + "\n")
            stat.write("time: " + self.__matrix_time[i].__str__() + "\n")
        stat.write("all time: " + np.sum(self.__matrix_time, axis=0).__str__())
        stat.close()

    def __validation(self, path_test, path_reference, path_cmp):
        is_valid = True
        is_valid &= os.path.isfile(self.__program)
        is_valid &= len(params) == 2
        if not os.path.isdir(self.__output):
            self.__output = os.getcwd() + "\\results"
        is_valid &= os.path.exists(self.path_test)
        is_valid &= os.path.exists(self.path_reference) | path_reference == ""
        if os.path.isfile(self.path_cmp):
            cmp = __is_equal_file_user(path_cmp)
        else:
            cmp = __is_equal_file_default
            return is_valid

    def start_test_by_path(self, path_exe, path_test, params, path_res, path_reference, path_cmp):
        self.__program = path_exe
        self.__params = params
        self.__output = path_res
        if not self.__validation(path_test, path_reference, path_cmp):
            return None
        shutil.rmtree(self.__output)
        os.mkdir(self.__output)
        self.__output += "\\"

        tests = [""]
        if path_test.find(".") == -1:  # check path_test is fold or file
            tests = os.listdir(path_test)
            path_test += "\\"

        if path_reference == "":
            self.__start_tests(path_test, tests)
            return Data(__matrix_time, __matrix_is_complete, path_test + "statistic.txt")

        reference = [""]
        if path_reference.find(".") == -1:  # check path_etalon is fold or file
            reference = os.listdir(path_reference)
            path_reference += "\\"

        self.__start_tests(path_test, tests, self.__params, path_reference, reference, self.__cmp)
        return Data(__matrix_time, __matrix_is_complete, path_test + "statistic.txt")


# Next code is UI

class MainWindow(QWidget):
    kernel = Kernel()
    data = []

    def __init__(self):
        super().__init__()
        self.result = None
        main_horizontal_layout = QHBoxLayout()

        main_vertical_layout = QVBoxLayout()

        test_scenario_label = QLabel("Test scenario path")
        self.test_scenario_path = QLineEdit()

        path_tests_label = QLabel("Path to file(folder) with test(tests)")
        self.path_tests_path = QLineEdit()

        test_params_layout = QHBoxLayout()
        test_params_layout.addStretch(2)
        self.test_params_label = QLabel("Current Param value")
        self.test_params_value = QLineEdit()
        self.test_params_value.textChanged.connect(self.on_value_changed)
        test_params_layout.addWidget(self.test_params_label)
        test_params_layout.addWidget(self.test_params_value)

        self.test_params_slider = QSlider(Qt.Horizontal, self)
        self.test_params_slider.setFocusPolicy(Qt.StrongFocus)
        self.test_params_slider.setTickPosition(QSlider.TicksBothSides)
        self.test_params_slider.setTickInterval(1)
        self.test_params_slider.setSingleStep(1)
        self.test_params_slider.setMinimum(0)
        self.test_params_slider.setMaximum(100)
        self.test_params_slider.setValue(50)
        self.test_params_slider.valueChanged[int].connect(self.on_slider_changed)

        path_answers_label = QLabel("Path to default test answers")
        self.path_answers_path = QLineEdit()

        path_result_label = QLabel("Path to save answers folder")
        self.path_result_path = QLineEdit()

        path_comp_label = QLabel("Path to answers comparator file")
        self.path_comp_path = QLineEdit()

        calc_button = QPushButton("Calc")
        calc_button.clicked.connect(self.on_calc_click)

        main_vertical_layout.addWidget(test_scenario_label)
        main_vertical_layout.addWidget(self.test_scenario_path)
        main_vertical_layout.addWidget(path_tests_label)
        main_vertical_layout.addWidget(self.path_tests_path)
        main_vertical_layout.addLayout(test_params_layout)
        main_vertical_layout.addWidget(self.test_params_slider)
        main_vertical_layout.addWidget(path_answers_label)
        main_vertical_layout.addWidget(self.path_answers_path)
        main_vertical_layout.addWidget(path_result_label)
        main_vertical_layout.addWidget(self.path_result_path)
        main_vertical_layout.addWidget(path_comp_label)
        main_vertical_layout.addWidget(self.path_comp_path)
        main_vertical_layout.addWidget(calc_button)

        main_horizontal_layout.addLayout(main_vertical_layout)

        self.setLayout(main_horizontal_layout)
        self.setGeometry(300, 200, 1280, 720)
        self.setWindowTitle('QLineEdit')

    def on_slider_changed(self):
        self.test_params_value.setText(str(self.test_params_slider.value()))

    def on_value_changed(self):
        try:
            temp_value = int(self.test_params_value.text())
        except ValueError:
            temp_value = 0
        self.test_params_slider.setValue(temp_value)

    def on_calc_click(self):
        one_data = [
            [TestConfiguration("test one", random.random(), random.random(), i + 1, i + 1) for i in range(10)],
            [TestConfiguration("test two", random.random(), random.random(), i + 1, i + 1) for i in range(10)],
            [TestConfiguration("test three", random.random(), random.random(), i + 1, i + 1) for i in range(10)],
            [TestConfiguration("test four", random.random(), random.random(), i + 1, i + 1) for i in range(10)]
        ]
        path_exe = self.test_scenario_path.text()
        path_test = self.path_tests_path.text()
        params = self.test_params_slider.value()
        path_reference = self.path_answers_path.value()
        path_res = self.path_result_path.value()
        cmp = self.path_comp_path.value()
        res = self.kernel.start_test_by_path(path_exe, path_test, params, path_res, path_reference, cmp)

        if (res == None):
            do_smth = "print param is invalid"
        else:
            data.append(res)
        # Here will be request to backend
        self.result = ResultWindow(one_data)
        self.result.show()


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
                self.get_result_item(result_data[i], self.on_curve_show_change, i)
            )

        self.result = result_data

        group_box = QGroupBox()
        group_box.setLayout(self.result_list)
        self.scroll = QScrollArea()
        self.scroll.setWidget(group_box)
        self.scroll.setWidgetResizable(True)

        self.curve_status_show = [True for i in range(len(result_data))]

        self.result_graph = PlotCanvas(width=7, height=7, curve_status_show=self.curve_status_show, data=result_data)
        self.main_horizontal_layout = QHBoxLayout()
        self.main_horizontal_layout.setAlignment(Qt.AlignRight)
        self.main_horizontal_layout.addWidget(self.scroll)
        self.main_horizontal_layout.addWidget(self.result_graph)

        self.setLayout(self.main_horizontal_layout)

    def on_curve_show_change(self, number_of_curve, status):
        self.curve_status_show[number_of_curve] = status
        self.main_horizontal_layout.removeWidget(self.result_graph)
        self.result_graph = PlotCanvas(width=7, height=7, curve_status_show=self.curve_status_show, data=self.result)
        self.main_horizontal_layout.addWidget(self.result_graph)

    def get_result_item(self, data_list, call_back_checkbox, number_of_test):
        item_layout = QHBoxLayout()
        item_check_box = QCheckBox()
        item_check_box.setChecked(True)
        item_check_box.stateChanged.connect(
            # lambda arg1=number_of_test, arg2=item_check_box.isChecked: call_back_checkbox(arg1, arg2()))
            self.template(number_of_test, item_check_box.isChecked))
        item_layout.addWidget(item_check_box)
        sub_items_layout = QVBoxLayout()
        for data in data_list:
            sub_record_layout = QHBoxLayout()
            item_name = QLabel(str(data.name))
            item_time = QLabel(str(data.time))
            item_status = QLabel(str(data.status))
            item_number = QLabel(str(data.number))
            item_number_cores = QLabel(str(data.count_of_cores))

            sub_record_layout.addWidget(item_name)
            sub_record_layout.addWidget(item_time)
            sub_record_layout.addWidget(item_status)
            sub_record_layout.addWidget(item_number)
            sub_record_layout.addWidget(item_number_cores)

            sub_items_layout.addLayout(sub_record_layout)
        item_layout.addLayout(sub_items_layout)

        return item_layout


class PlotCanvas(FigureCanvas):

    def __init__(self, width=7, height=7, dpi=80, data=None, curve_status_show=[]):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)

        self.plot(data, curve_status_show)
        self.draw()

    def plot(self, data_list, curve_status_show):
        ax = self.figure.add_subplot(111)
        for test in range(len(data_list)):
            if curve_status_show[test]:
                # Question with indexes
                x = np.array([current_test.count_of_cores for current_test in data_list[test]])
                y = np.array([current_test.time for current_test in data_list[test]])
                ax.plot(x, y)

        ax.set_ylabel("Execution time")
        ax.set_xlabel("Count of Cores")
        ax.grid()
        ax.set_title(str(curve_status_show[0]))


class TestConfiguration:
    def __init__(self, name, time, status, number, count_of_cores):
        self.name = name
        self.time = time
        self.status = status
        self.number = number
        self.count_of_cores = count_of_cores


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
    # main()

    # result_path =  path
# os.system(program)
# path = os.getcwd() + "\\folder"
# stat = open(path + "\\statistica.txt", 'w')
# data = {
#    "param": {
#    "from": params[0],
#    "to": params[1]
#    }
# }
# json.dump(data, stat)

# f1 = np.array([1, 2, 3, 4, 5]).__str__()
# f2 = np.array([True, False, True, True, False]).__str__()
# dic = {}
# dic["test1"] = [f1, f2]
# json.dump(dic, stat)
# stat.close()
# path = os.getcwd() + "\\folder"
# shutil.rmtree(path)
# os.mkdir(path + "aaa")
# t = os.listdir(os.getcwd())
# i = 7
# args = {'index': i}
# u = 'path %(index)s'
# print(u % args)