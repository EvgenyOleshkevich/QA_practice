import difflib
import os
import random
import subprocess
import time
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import shutil
import json

program = ""
params = [0, 100]
matrix_time = np.array([])
matrix_is_complete = np.array([])

def is_equal_file_default(path1, path2):
    file1 = open(path_res, 'r')  # tyt nado ykazuvat to chto nakhoditsa pod somneniem
    file2 = open(etalon, 'r')  # tyt etalon
    diff = difflib.ndiff(file1.readlines(), file2.readlines())
    return ''.join(x for x in diff if x.startswith('- ')) == ""

def is_equal_file_true(path1, path2): return True
def is_equal_file_user(path):
    def func(path1, path2):
        return subprocess.check_output([path, path1, path2])

cmp = is_equal_file_default

def execute_test(test, res_i, etalon):
    time_work = -1 * np.ones(param[1] + 1 - param[0])
    is_complete = np.array([False ] * (param[1] + 1 - param[0]))
    for i in range(0, param[1] + 1 - param[0]):
        param = (i + params[0]).__str__()
        res = res_i + "\\" + param + ".txt"
        timer = time.clock()
        #subprocess.check_call([program, param, test, res]) with exception
        subprocess.call([program, param, test, res]) # without exception
        time_work[i] = time.clock() - timer
        is_complete[i] = cmp(path_res, etalon)
    return time_work, is_complete

def execute_test(test): # without output
    time_work = -1 * np.ones(param[1] + 1 - param[0])
    for i in range(0, param[1] + 1 - param[0]):
        timer = time.clock()
        subprocess.call([program, (i + params[0]).__str__(), test])
        time_work[i] = time.clock() - timer
    return time_work

def start_tests(path_test, tests, path_res, path_etalon, etalons):
    matrix_time = np.array(len(tests))
    matrix_is_complete = np.array(len(tests))
    stat = open(path_res + "\\statistica.txt", 'w')
    for i in range(0, len(tests)):
        test = path_test + tests[i]
        etalon = path_etalon + etalons[i]
        res = path_res + "\\" + i.__str__()
        os.mkdir(res)
        matrix[i], matrix_is_complete[i] = execute_test(test, res, etalon)
        stat.write(tests[i] + "\n")
        stat.write("time: " + matrix_time[i].__str__() + "\n")
        stat.write("result: " + matrix_is_complete[i].__str__() + "\n")
    stat.write("all time: " + np.sum(matrix_time, axis = 0).__str__())
    stat.close()

def start_tests(path_test, tests):
    matrix = np.array(len(tests))
    for i in range(0, len(tests)):
        test = path_test + tests[i]
        matrix[i] = execute_test(test)
        stat.write(tests[i] + "\n")
        stat.write("time: " + matrix_time[i].__str__() + "\n")
    stat.write("all time: " + np.sum(matrix_time, axis = 0).__str__())
    stat.close()

def get_time(mask):
    return np.sum(matrix_time[mask], axis = 0)

def get_time_tests(index):
    return matrix_time[index]

def get_results_tests(index):
    return matrix_complete[index]

def main(path_test):
    tests = [""]
    if path_test.find(".") == -1: # check path_test is fold or file
        tests = os.listdir(path_test)
        path_test += "\\"
    start_tests(path_test, tests)

def main(path_exe, path_test, _params, path_res = os.getcwd() + "\\results", path_etalon = "", path_cmp = ""):
    program = path_exe
    params = _params
    if path_etalon == "":
        main(path_test)
        return
    shutil.rmtree(path_res)
    os.mkdir(path_res)
    tests = [""]
    if path_test.find(".") == -1: # check path_test is fold or file
        tests = os.listdir(path_test)
        path_test += "\\"

    etalons = [""]
    if path_etalon.find(".") == -1: # check path_etalon is fold or file
        etalons = os.listdir(path_etalon)
        path_etalon += "\\"

    if path_cmp != "":
        cmp = is_equal_file_user(path_cmp)
    start_tests(path_test, tests, params, path_res, path_etalon, etalons, cmp)

def old_main():
    path = input()
    program = path + "\\main.exe"
    t = os.listdir(path + "\\test")
    files_test = []
    for test in t:
        files_test.append(path + "\\test\\" + test)
    t = os.listdir(path + "\\check")
    files_check = []
    for test in t:
        files_check.append(path + "\\check\\" + test)
    tests = np.append([[], []], [files_test, files_check], axis=1).transpose()
    out_path = path + "\\out\\out.txt"
    с(program, tests, out_path, 4)
    # result_path =  path

    # os.system(program)
path = os.getcwd() + "\\folder"
stat = open(path + "\\statistica.txt", 'w')
data = {
     "param": {
     "from": params[0],
     "to": params[1]
     }
}
json.dump(data, stat)

f1 = np.array([1, 2, 3, 4, 5]).__str__()
f2 = np.array([True, False, True, True, False]).__str__()
dic = {}
dic["test1"] = [f1, f2]
json.dump(dic, stat)
stat.close()
path = os.getcwd() + "\\folder"
shutil.rmtree(path)
os.mkdir(path + "aaa")
t = os.listdir(os.getcwd())
i = 7
args = {'index': i}
u = 'path %(index)s'
print(u % args)


# Next code is UI
class MainWindow(QWidget):

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
