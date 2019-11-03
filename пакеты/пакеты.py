import difflib
import os
import subprocess
import time

import matplotlib.pyplot as plt
import numpy as np
program = ""

def is_equal_file_default(path1, path2):
    file1 = open(path_res, 'r')  # tyt nado ykazuvat to chto nakhoditsa pod somneniem
    file2 = open(etalon, 'r')  # tyt etalon
    diff = difflib.ndiff(file1.readlines(), file2.readlines())
    return ''.join(x for x in diff if x.startswith('- ')) == ""

def is_equal_file_true(path1, path2): return True

def Testing(test, res_i, etalon, paprams, cmp):
    time_work = -1 * np.ones(param[1] + 1 - param[0])
    is_complete = np.array([False ] * (param[1] + 1 - param[0]))
    for i in range(0, param[1] + 1 - param[0]):
        param = (i + params[0]).__str__()
        res = res_i + param
        timer = time.clock()
        subprocess.check_call([program, param, test, res])
        time_work[i] = time.clock() - timer
        is_complete[i] = cmp(path_res, etalon)
    return [time_work, is_complete]

def Testing(test, papram): # without output
    time_work = -1 * np.ones(param[1] + 1 - param[0])
    for i in range(0, param[1] + 1 - param[0]):
        timer = time.clock()
        subprocess.check_call([program, (i + params[0]).__str__(), test])
        time_work[i] = time.clock() - timer
    return time_work

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
i = 7
args = {'index': i}
u = 'path %(index)s'
print(u % args)


if __name__ == "__main__":
    main()
