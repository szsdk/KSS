import numpy as np
import logging
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
#logging.basicConfig(format=FORMAT,level=logging.DEBUG)
#logging.basicConfig(filename='log',format=FORMAT,level=logging.INFO)
logging.basicConfig(format=FORMAT,level=logging.INFO)

class Parameter(object):
    def __init__(self, **args):
        self.__ignore=set([])
        for k, v in args.items():
            self.__dict__[k] = v

    def ignore(self):
        return self.__ignore

    def set_ignore(self, ignore):
        self.__ignore=ignore

    def __str__(self):
        s=''
        for i, v in self.__dict__.items():
            s+='%s:%s\n' % (i, v)
        return s

    def __eq__(self, other, debug=False):
        self_keys = set(self.__dict__.keys())-self.ignore()
        other_keys = set(other.__dict__.keys())-other.ignore()
        if debug:
            if self_keys-other_keys :
                logging.warning('%s just in the left one', self_keys-other_keys)
            if other_keys-self_keys:
                logging.warning('%s just in the right one', other_keys-self_keys)
        ans=True
        for i in self_keys & other_keys:
            if not '_' in i and not np.array_equal(self.__dict__[i],other.__dict__[i]):
                if debug:
                    logging.warning('Left:%s=%s Right:%s=%s', i, self.__dict__[i], i, other.__dict__[i])
                    ans=False
                else:
                    return False
        return ans

import pickle
def save_data(filename, para, data):
    with open(filename, 'wb') as f:
        pickle.dump(para, f)
        pickle.dump(data, f)

def get_parameter(filename):
    with open(filename, 'rb') as f:
        para = pickle.load(f)
    return para

def read_data(filename):
    with open(filename, 'rb') as f:
        para = pickle.load(f)
        data = pickle.load(f)
    return para, data
