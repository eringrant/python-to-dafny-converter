import nose
import translate
import ast


class TestTranslate(unittest.TestCase):

    def test_translate_one_arg(self):
        """Test translate on a function with one argument value, no return
        value, no preconditions, and no postconditions.
        """

        with open('identity_function.py') as f:
            source = f.readlines()

        with open('identity_function.py.dafny') as f:
            expected = f.readlines()

        tree = ast.parse(source, 'eval')
        actual = translate.translate(tree)

        self.assertEqual(actual, expected)
