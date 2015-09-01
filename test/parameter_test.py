import sys
sys.path.append('..')

from parameter import Parameter
import unittest

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

unittest.main()
