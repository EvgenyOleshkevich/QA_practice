import difflib
import os
import random
import shutil
import subprocess
import sys
import time

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Data:
    matrix_time = None
    matrix_is_complete = None
    path_statistic = None

    def get_time(self, mask): return np.sum(self.matrix_time[mask], axis=0)

    def get_time_tests(self, index): return self.matrix_time[index]

    def get_results_tests(self, index): return self.matrix_is_complete[index]

    def clear_data(self):
        self.matrix_time.clear()
        self.matrix_is_complete.clear()

    def download_data(self):
        file = open(self.path_statistic, 'r')
        b, g = file.readline()
        # finish writing

    def __init__(self, matrix_time, matrix_is_complete, path_statistic):
        super().__init__()
        self.matrix_time = matrix_time
        self.matrix_is_complete = matrix_is_complete
        self.path_statistic = path_statistic


class Kernel:

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

    def __init__(self):
        self.__program = ""
        self.__output = ""
        self.params = np.array([int(1), int(1)])
        self.__matrix_time = np.array([])
        self.__matrix_is_complete = np.array([])
        self.__progress_callback = None
        self.__complete = 0
        self.__count_tests = 0
        self.__cmp = self.__is_equal_file_default

    # array = [True for i in range(n)]

    def __execute_test(self, test, res_i, reference):
        time_work = -1 * np.ones(int(self.params[1] + 1 - self.params[0]))
        is_complete = np.array([False for i in range(int(self.params[1] + 1 - self.params[0]))])
        for i in range(int(self.params[1] + 1 - self.params[0])):
            param = (i + self.params[0]).__str__()
            res = res_i + "\\" + param + ".txt"
            timer = time.clock()
            # subprocess.check_call([__program, param, test, res]) with exception
            subprocess.call([self.__program, param, test, res])  # without exception
            time_work[i] = time.clock() - timer
            is_complete[i] = self.__cmp(res, reference)
            self.__complete += 1
            self.__progress_callback(self.__complete, self.__count_tests)
        return [time_work, is_complete]

    def __execute_test_wo_ref(self, test):  # without output
        time_work = -1 * np.ones(int(self.params[1] + 1 - self.params[0]))
        for i in range(int(self.params[1] + 1 - self.params[0])):
            timer = time.clock()
            subprocess.call([self.__program, (i + self.params[0]).__str__(), test])
            time_work[i] = time.clock() - timer
            self.__complete += 1
            self.__progress_callback(self.__complete, self.__count_tests)
        return time_work

    def __start_tests(self, path_test, tests, path_reference, references):
        self.__matrix_time = np.array([np.zeros(self.params[1] + 1 - self.params[0])])
        self.__matrix_is_complete = np.array([np.zeros(self.params[1] + 1 - self.params[0])])
        stat = open(self.__output + "statistic.txt", 'w')
        stat.write(self.params.__str__() + "\n")
        for i in range(0, len(tests)):
            test = path_test + tests[i]
            reference = path_reference + references[i]
            res = self.__output + i.__str__()
            os.mkdir(res)
            a, b = self.__execute_test(test, res, reference)
            self.__matrix_time = np.append(self.__matrix_time, [a], axis=0)
            self.__matrix_is_complete = np.append(self.__matrix_is_complete, [b], axis=0)
            # self.__matrix_is_complete[i] = b
            stat.write(tests[i] + "\n")
            stat.write("time: " + self.__matrix_time[i + 1].__str__() + "\n")
            stat.write("result: " + self.__matrix_is_complete[i + 1].__str__() + "\n")
        self.__matrix_time = np.delete(self.__matrix_time, 0, axis=0)
        self.__matrix_is_complete = np.delete(self.__matrix_is_complete, 0, axis=0)
        stat.write("all time: " + np.sum(self.__matrix_time, axis=0).__str__())
        stat.close()

    def __start_tests_wo_ref(self, path_test, tests):
        self.__matrix_time = np.array(len(tests))
        stat = open(self.__output + "statistic.txt", 'w')
        for i in range(0, len(tests)):
            test = path_test + tests[i]
            self.__matrix_time[i] = self.__execute_test_wo_ref(test)
            stat.write(tests[i] + "\n")
            stat.write("time: " + self.__matrix_time[i].__str__() + "\n")
        stat.write("all time: " + np.sum(self.__matrix_time, axis=0).__str__())
        stat.close()

    def __validation(self, path_test, path_reference, path_cmp):
        is_valid = True
        is_valid &= os.path.isfile(self.__program)
        is_valid &= len(self.params) == 2
        if not os.path.isdir(self.__output):
            self.__output = os.getcwd() + "\\results"
        is_valid &= os.path.exists(path_test)
        is_valid &= path_reference == "" or os.path.exists(path_reference)
        if os.path.isfile(path_cmp):
            self.__cmp = self.__is_equal_file_user(path_cmp)
        return is_valid

    def start_test_by_path(self, path_exe, path_test, params, path_res, path_reference, path_cmp, lambda_callback):
        self.__program = path_exe
        self.params[1] = int(params)
        self.__output = path_res
        self.__progress_callback = lambda_callback
        if not self.__validation(path_test, path_reference, path_cmp):
            return None
        if os.path.isdir(self.__output):
            shutil.rmtree(self.__output)
        os.mkdir(self.__output)
        self.__output += "\\"

        tests = [""]
        if path_test.find(".") == -1:  # check path_test is fold or file
            tests = os.listdir(path_test)
            path_test += "\\"

        self.__complete = 0
        self.__count_tests = len(tests) * (self.params[1] - self.params[0] + 1)

        if path_reference == "":
            self.__start_tests_wo_ref(path_test, tests)
            return Data(self.__matrix_time, self.__matrix_is_complete, path_test + "statistic.txt")

        reference = [""]
        if path_reference.find(".") == -1:  # check path_reference is    fold or file
            reference = os.listdir(path_reference)
            path_reference += "\\"

        self.__start_tests(path_test, tests, path_reference, reference)
        return Data(self.__matrix_time, self.__matrix_is_complete, path_test + "statistic.txt")


# Next code is UI


class ProgressWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.main_vertical_layout = QVBoxLayout()
        self.progress_bar = QProgressBar(self)
        self.progress_label = QLabel("Сделано столько то тестов")
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
    kernel = Kernel()
    data = []

    def __init__(self):
        super().__init__()
        self.error_window = ErrorWindow()
        self.progressive_window = ProgressWindow()
        self.result = None
        main_horizontal_layout = QHBoxLayout()

        main_vertical_layout = QVBoxLayout()

        test_scenario_label = QLabel("Test scenario path")
        self.test_scenario_path = QLineEdit()

        path_tests_label = QLabel("Path to file(folder) with test(tests)")
        self.path_tests_path = QLineEdit()

        test_params_layout = QHBoxLayout()
        test_params_layout.addStretch(0)
        self.test_params_label = QLabel("Current Param value")
        self.test_params_value = QLineEdit()
        self.test_params_value.textChanged.connect(self.on_value_changed)
        test_params_layout.addWidget(self.test_params_label)
        test_params_layout.addWidget(self.test_params_value)
        test_params_layout.addStretch(20)

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
        main_vertical_layout.addStretch(0)
        main_vertical_layout.addWidget(self.test_params_slider)
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
        main_vertical_layout.addWidget(calc_button)

        main_horizontal_layout.addLayout(main_vertical_layout)

        self.setLayout(main_horizontal_layout)
        self.setGeometry(300, 200, 1280, 720)
        self.setWindowTitle('QLineEdit')

    # def on_test_progress(self):

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
            [TestConfiguration("test one", random.random(), "Complete", i + 1, i + i * i) for i in range(10)],
            [TestConfiguration("test two", random.random(), "Complete", i + 1, i + i * i) for i in range(10)],
            [TestConfiguration("test three", random.random(), "Complete", i + 1, i + i * i) for i in range(10)],
            [TestConfiguration("test four", random.random(), "Complete", i + 1, i + i * i) for i in range(10)]
        ]
        # path_exe = self.test_scenario_path.text()
        # "C:\\Users\\Vladimir\\Desktop\\QA_practice\\пакеты\\test\\test"
        path_exe = "C:\\Users\\Vladimir\\Desktop\\QA_practice\\пакеты\\test\\main.exe"
        # path_test = self.path_tests_path.text()
        path_test = "C:\\Users\\Vladimir\\Desktop\\QA_practice\\пакеты\\test\\test"
        params = 4  # self.test_params_slider.value()
        path_reference = "C:\\Users\\Vladimir\\Desktop\\QA_practice\\пакеты\\test\\reference"
        # self.path_answers_path.text()
        path_res = self.path_result_path.text()
        cmp = self.path_comp_path.text()

        # self.progressive_window.show()
        result = self.kernel.start_test_by_path(path_exe, path_test, params, path_res, path_reference, cmp,
                                                self.progressive_window.get_test_setter())
        # self.progressive_window.close()

        if result is None:
            self.error_window.show()
        else:
            self.data.append(result)
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
                self.get_result_item(result_data[i], i)
            )
            self.result_list.addSpacing(35)

        self.result = result_data

        group_box = QGroupBox()
        group_box.setLayout(self.result_list)
        self.scroll = QScrollArea()
        self.scroll.setWidget(group_box)
        self.scroll.setWidgetResizable(True)

        self.curve_status_show = [True for i in range(len(result_data))]

        self.result_graph = PlotCanvas(width=10, height=10, curve_status_show=self.curve_status_show, data=result_data)
        self.main_horizontal_layout = QHBoxLayout()
        self.main_horizontal_layout.setAlignment(Qt.AlignRight)
        self.main_horizontal_layout.addWidget(self.scroll)
        self.main_horizontal_layout.addWidget(self.result_graph)
        self.main_horizontal_layout.setAlignment(Qt.AlignLeft)

        self.setLayout(self.main_horizontal_layout)

    def on_curve_show_change(self, number_of_curve, status):
        self.curve_status_show[number_of_curve] = status
        self.main_horizontal_layout.removeWidget(self.result_graph)
        self.result_graph.resize(0, 0)
        self.result_graph = PlotCanvas(width=10, height=10, curve_status_show=self.curve_status_show, data=self.result)
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
            item_name = QLabel(str(data.name))
            item_time = QLabel(f"Execution time: {round(data.time, 6)}")
            item_status = QLabel(str(data.status))
            item_number = QLabel(str(data.number))
            item_number_cores = QLabel(f"Count of cores: {data.count_of_cores}")

            sub_record_layout.addWidget(item_name)
            sub_record_layout.addWidget(item_time)
            sub_record_layout.addWidget(item_status)
            sub_record_layout.addWidget(item_number)
            sub_record_layout.addWidget(item_number_cores)

            sub_items_layout.addLayout(sub_record_layout)
        item_layout.addLayout(sub_items_layout)
        item_layout.addStretch(0)
        return item_layout


class PlotCanvas(FigureCanvas):

    def __init__(self, width=7, height=7, dpi=80, data=None, curve_status_show=None):
        if curve_status_show is None:
            curve_status_show = []
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)

        self.plot(data, curve_status_show)
        self.draw()

    def plot(self, data_list, curve_status_show):
        ax = self.figure.add_subplot(111)
        for test in range(len(data_list)):
            if curve_status_show[test]:
                x = np.array([current_test.count_of_cores for current_test in data_list[test]])
                y = np.array([current_test.time for current_test in data_list[test]])
                ax.plot(x, y, label=f"Test №{test + 1}")

        ax.legend()
        ax.set_ylabel("Execution time")
        ax.set_xlabel("Count of Cores")
        ax.grid()
        ax.set_title("Tasks Graph")


class ErrorWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Input data is not valid!"))
        self.setLayout(layout)
        self.setGeometry(600, 500, 200, 50)
        self.setWindowTitle("Error!")


class TestConfiguration:
    def __init__(self, name, time_stat, status, number, count_of_cores):
        self.name = name
        self.time = time_stat
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
