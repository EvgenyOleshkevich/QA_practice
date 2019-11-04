import difflib
import os
import shutil
import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np
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


if __name__ == "__main__":
    main()
