import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metis.metis import MetisClass
import metis.example.generate_example as ex
if __name__ == '__main__':

    ex.create_example_py_file()
