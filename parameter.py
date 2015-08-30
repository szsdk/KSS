import numpy as np
import logging
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
#logging.basicConfig(format=FORMAT,level=logging.DEBUG)
#logging.basicConfig(filename='log',format=FORMAT,level=logging.INFO)
logging.basicConfig(format=FORMAT,level=logging.INFO)

class Parameter(object):
    def __init__(self, debug=False, strict=False, **args):
        self.__ignore=set([])
        self.__debug = debug
        self.__strict = strict
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

    def __eq__(self, other, **args):
        debug = args['debug'] if 'debug' in args else self.__debug 
        strict = args['strict'] if 'strict' in args else self.__strict 
        #if 'strict' in args:
            #strict = args['strict']
        #else:
            #strict = self.__strict 
        if not strict:
            self_keys = set(self.__dict__.keys())-self.ignore()
            other_keys = set(other.__dict__.keys())-other.ignore()
        else:
            self_keys = set(self.__dict__.keys())
            other_keys = set(other.__dict__.keys())

        ans=True
        if self_keys-other_keys :
            logging.warning('%s just in the left one', self_keys-other_keys)
            if strict:
                if debug:
                    ans = False
                else:
                    return False
        if other_keys-self_keys:
            logging.warning('%s just in the right one', other_keys-self_keys)
            if strict:
                if debug:
                    ans = False
                else:
                    return False

        if strict:
            for i in self_keys & other_keys:
                if not np.array_equal(self.__dict__[i],other.__dict__[i]):
                    logging.warning('Left:%s=%s Right:%s=%s', i, self.__dict__[i], i, other.__dict__[i])
                    if debug:
                        ans=False
                    else:
                        return False
        else:
            for i in self_keys & other_keys:
                if not '_' in i and not np.array_equal(self.__dict__[i],other.__dict__[i]):
                    logging.warning('Left:%s=%s Right:%s=%s', i, self.__dict__[i], i, other.__dict__[i])
                    if debug:
                        ans=False
                    else:
                        return False
        return ans


a=Parameter(strict=True, h=12, c=23)
b=Parameter(h=12, c=23)
b.set_ignore({'h'})
a.set_ignore({'h'})
print(b.__dict__.keys())
print(a.__eq__(b))
