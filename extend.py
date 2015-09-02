from ctypes import *
import os
import numpy as np
from numpy.ctypeslib import ndpointer 
from subprocess import check_output
from contextlib import contextmanager
import io
import os,sys
import tempfile
import pickle

#check_output("gcc -std=c99 -c times.c", shell=True)
#check_output("gcc -shared times.o -o times.dll", shell=True)

#times = cdll.LoadLibrary(os.getcwd()+"/times.dll")
#print(times.multiply(3,3))

@contextmanager
def stdout_redirected(to=os.devnull):
    '''
    import os

    with stdout_redirected(to=filename):
        print("from Python")
        os.system("echo non-Python applications are also supported")
    '''
    fd = sys.stdout.fileno()

    ##### assert that Python and C stdio write using the same file descriptor
    ####assert libc.fileno(ctypes.c_void_p.in_dll(libc, "stdout")) == fd == 1

    def _redirect_stdout(to):
        sys.stdout.close() # + implicit flush()
        os.dup2(to.fileno(), fd) # fd writes to 'to' file
        sys.stdout = os.fdopen(fd, 'w') # Python writes to fd

    with os.fdopen(os.dup(fd), 'w') as old_stdout:
        #temp = tempfile.NamedTemporaryFile(mode='w')
        #_redirect_stdout(to=temp)
        with open(to, 'w') as file:
            _redirect_stdout(to=file)
        try:
            yield # allow code to be run with the redirected stdout
        finally:
            _redirect_stdout(to=old_stdout) # restore stdout.
                                            # buffering and flags such as
                                            # CLOEXEC may be different

def to_c_2Darray(m):
    return (m.__array_interface__['data'][0] 
         + np.arange(m.shape[0])*m.strides[0]).astype(np.uintp)

c_2Darray= ndpointer(dtype=np.uintp, ndim=1, flags='C') 
