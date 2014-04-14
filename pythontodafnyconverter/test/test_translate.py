import os
import unittest
import nose
import pythontodafnyconverter.translate
import ast


class TestTranslate(unittest.TestCase):

    def test_translate_one_arg(self):
        """Test translate on a function with one argument value, no return
        value, no preconditions, and no postconditions.
        """

        with open("/home/erin/Git/PythonToDafnyConverter/pythontodafnyconverter/test/identity_function.py") as f:
            source = f.read()

        actual = pythontodafnyconverter.translate.initiate_translation(source)

        with open('./test/identity_function.py.dafny') as f:
            expected = f.read()

        self.assertEqual(actual, expected)

