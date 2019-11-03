import difflib
import os
import subprocess
import time
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QLabel, QLineEdit, QSlider)

import matplotlib.pyplot as plt
import numpy as np


def Testing(program, test, path_res, etalon, count):
    res = []
    for i in range(1, count + 1):
        timer = time.clock()
        subprocess.check_call([program, i.__str__(), test, path_res])
        timer = time.clock() - timer
        file1 = open(path_res, 'r')  # tyt nado ykazuvat to chto nakhoditsa pod somneniem
        file2 = open(etalon, 'r')  # tyt etalon

        diff = difflib.ndiff(file1.readlines(), file2.readlines())
        delta = ''.join(x for x in diff if x.startswith('- '))
        if delta == "":
            res.append(timer)
        else:
            res.append(-1)
    return res


def с(program, tests, path_res, count):  # test = [test, etalon]
    matrix = []
    for test in tests:
        matrix.append(Testing(program, test[0], path_res, test[1], count))
    axis_x = [(i + 1) for i in range(count)]
    fig, ax = plt.subplots()
    for line in matrix:
        # plt.plot(axisX, line)
        ax.plot(axis_x, line, color='black', linewidth=1)
    # ax.scatter([0, 1, 2, 3, 4], [1, 3, 8, 12, 27], color = 'blue', marker = '*')
    plt.show()


def main():
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


class Example(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        test_scenario_label = QLabel("Test scenario path")
        self.test_scenario_path = QLineEdit()

        path_tests_label = QLabel("Path to file(folder) with test(tests)")
        self.path_tests_path = QLineEdit()

        self.test_params_label = QLabel("Params")

        self.test_params_slider = QSlider(Qt.Horizontal, self)
        self.test_params_slider.setFocusPolicy(Qt.StrongFocus)
        self.test_params_slider.setTickPosition(QSlider.TicksBothSides)
        self.test_params_slider.setTickInterval(1)
        self.test_params_slider.setSingleStep(1)
        self.test_params_slider.setMinimum(0)
        self.test_params_slider.setMaximum(100)
        self.test_params_slider.valueChanged[int].connect(self.on_slider_changed)

        path_answers_label = QLabel("Path to default test answers")
        self.path_answers_path = QLineEdit()

        path_result_label = QLabel("Path to save answers folder")
        self.path_result_path = QLineEdit()

        path_comp_label = QLabel("Path to answers comparator file")
        self.path_comp_path = QLineEdit()

        calc_button = QPushButton("Calc")
        calc_button.clicked.connect(self.on_calc_click)

        main_layout.addWidget(test_scenario_label)
        main_layout.addWidget(self.test_scenario_path)
        main_layout.addWidget(path_tests_label)
        main_layout.addWidget(self.path_tests_path)
        main_layout.addWidget(self.test_params_label)
        main_layout.addWidget(self.test_params_slider)
        main_layout.addWidget(path_answers_label)
        main_layout.addWidget(self.path_answers_path)
        main_layout.addWidget(path_result_label)
        main_layout.addWidget(self.path_result_path)
        main_layout.addWidget(path_comp_label)
        main_layout.addWidget(self.path_comp_path)
        main_layout.addWidget(calc_button)

        self.setLayout(main_layout)
        self.setGeometry(300, 200, 1280, 720)
        self.setWindowTitle('QLineEdit')

    def on_slider_changed(self):
        self.test_params_label.setText(self.test_params_slider.value())
    def on_calc_click(self):
        print(self.test_params_slider.value())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = Example()
    ex.show()
    sys.exit(app.exec_())
    # main()
