import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # add metisse to path
import metisse.example.generate_example as ex
from metisse.metisse import MetisseClass

if __name__ == "__main__":
    ex.create_example_py_file()
