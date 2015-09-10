import sys
sys.path.append('..')

from parameter import *
import unittest
import time
import numpy as np

class TestParameter(unittest.TestCase):

    def test_ignore(self):
        a=Parameter(h=1,v=32)
        b=Parameter(h=1, c=23, _b=33)
        b.set_ignore({'c'})

        self.assertTrue(a.__eq__(b,True))

        c = Parameter(h=12, c=23, a="jio")
        c.set_ignore({'a'})
        self.assertFalse(b.__eq__(c,True))

        d = Parameter(h=1, _b=23)
        self.assertTrue(d.__eq__(b,True))

    def test_save_data(self):
        a = Parameter(h=1,v=32)
        save_data('save_data.dat', a, [1,2,3])
        b = get_parameter('save_data.dat')
        self.assertTrue(a.__eq__(b,True))

    def test_speed(self):
        fn = 'save_data.dat'
        a=Parameter(h=1,v=32)
        save_data(fn, a, np.random.rand(100000))
        t = time.time()
        for _ in range(1000):
            get_parameter(fn)
        print("time:%.3f" % (time.time()-t))

        t = time.time()
        for _ in range(1000):
            read_data(fn)
        print("time:%.3f" % (time.time()-t))

unittest.main()
