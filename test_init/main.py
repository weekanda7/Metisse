import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.metis import MetisClass

if __name__ == '__main__':
    a = MetisClass('test', None, None , 'android')


