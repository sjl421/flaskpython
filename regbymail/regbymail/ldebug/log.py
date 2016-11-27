DEBUG = True

def log(log):
    if DEBUG:
        print(log)

import sys, traceback
def log_exception():
    traceback.print_exc(file=sys.stdout)
