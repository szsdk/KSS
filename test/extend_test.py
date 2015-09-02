import sys
sys.path.append("..")
import extend
from ctypes import *
import os
import numpy as np
from subprocess import check_output
import tempfile

import platform
if platform.system()=="Linux":
    check_output("gcc -std=c99 -fPIC -c times.c", shell=True)
    check_output("gcc -shared times.o -o times.so", shell=True)
    times = cdll.LoadLibrary(os.getcwd()+"/times.so")
else:
    check_output("gcc -std=c99 -c times.c", shell=True)
    check_output("gcc -shared times.o -o times.dll", shell=True)
    times = cdll.LoadLibrary(os.getcwd()+"/times.dll")

print(times.multiply(3,3))

trace=times.trace
trace.restype=c_int
trace.argtypes=[extend.c_2Darray,c_int]
print(trace(extend.to_c_2Darray(np.random.randint(4,size=[4,4])),4))

with tempfile.NamedTemporaryFile(mode='r', delete=False) as temp:
    with extend.stdout_redirected(temp.name):
        tr = trace(extend.to_c_2Darray(np.random.randint(4,size=[4,4])),4)
    a=np.loadtxt(temp.name)
print(a)
print(tr)
