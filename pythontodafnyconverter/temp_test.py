import sys
import os
import unittest
import ast

from translate import translate

if __name__ == '__main__':
    with open("./test/add_function.py") as f:
        source = f.read()

    actual = translate(source)

    with open('./test/add_function.py.dafny') as f:
        expected = f.read()

    print(actual)
    print(expected)
