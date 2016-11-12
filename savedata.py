import sys,os
import pickle
import logging
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT,level=logging.INFO)
from functools import wraps

class SaveData(object):
    '''
    This is the class the decorate a function for checking if
    the result file of this function exist, if not, computing
    and save it.
    '''
    folder = './'
    def __init__(self, save_to, refresh='never'):
        self.folder = ''
        self.filename = save_to
        if refresh in ['never', 'always', 'ask']:
            self.refresh = refresh
        else:
            raise ValueError("The refresh parameter should be 'never', 'always' or 'ask'.")

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwds):
            if self.folder:
                filename = self.folder+self.filename
            else:
                filename = SaveData.folder+self.filename

            ref = True
            if os.path.isfile(filename):
                if self.refresh == 'never':
                    ref = False
                if self.refresh == 'ask':
                    ref = SaveData.query_yes_no(
                    "Would you want to recalculate the %s" % self.filename,
                    default='no')

            if not ref:
                try:
                    logging.debug('try %s', filename)
                    _ = pickle.load(open(filename, 'rb'))
                except FileNotFoundError:
                    pass
                else:
                    logging.info('The file %s is existing.', filename)
                    return _
            logging.info('Computing %s', filename)
            #logging.info('Computing %s with %s', filename, self.func.__name__)
            _ = func(*args, **kwds)
            pickle.dump(_, open(filename, 'wb'), protocol=4)
            return _
        return wrapper

    @staticmethod
    def query_yes_no(question, default="yes"):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")
