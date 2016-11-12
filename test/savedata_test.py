import sys
sys.path.append('..')

from savedata import *
import unittest

@SaveData('f.dat', 'ask')
def f(a):
    return a+1

print(f(3))
