import matplotlib.pyplot as plt
import math
import numpy as np
import copy
import os
import subprocess
import time
import difflib

def Testing(program, test, pathRes, etalon, count):
    res = []
    for i in range(1, count + 1):
        timer = time.clock() 
        subprocess.check_call([program, i.__str__(), test, pathRes])
        timer = time.clock() - timer
        file1 = open(pathRes, 'r')#tyt nado ykazuvat to chto nakhoditsa pod somneniem
        file2 = open(etalon, 'r')#tyt etalon
 
        diff = difflib.ndiff(file1.readlines(), file2.readlines())
        delta = ''.join(x for x in diff if x.startswith('- '))
        if (delta == ""):
            res.append(timer)
        else:
            res.append(-1)
    return res

        
def с(program, tests, pathRes, count):#test = [test, etalon]
    matrix = []
    for test in tests:
        matrix.append(Testing(program, test[0], pathRes, test[1], count))
    axisX = [(i + 1) for i in range(count)]
    fig, ax = plt.subplots()
    for line in matrix:
        
        #plt.plot(axisX, line)
        ax.plot(axisX, line, color = 'black', linewidth = 1)
       # ax.scatter([0, 1, 2, 3, 4], [1, 3, 8, 12, 27], color = 'blue', marker = '*')
    plt.show()

def main():
    path = input();
    program  = path + "\\main.exe"
    t = os.listdir(path + "\\test")
    filesTest = []
    for test in t:
        filesTest.append(path + "\\test\\" + test)
    t = os.listdir(path + "\\check")
    filesCheck = []
    for test in t:
        filesCheck.append(path + "\\check\\" + test)
    tests = np.append([[],[]], [filesTest, filesCheck], axis = 1).transpose();
    out_path = path + "\\out\\out.txt"
    с(program, tests, out_path, 4)
    #result_path =  path

    
    
    #os.system(program)

if __name__ == "__main__":

   main();