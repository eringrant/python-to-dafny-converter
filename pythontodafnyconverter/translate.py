# This file is part of DafnyToPythonConverter.
#
# DafnyToPythonConverter is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DafnyToPythonConverter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with DafnyToPythonConverter.  If not, see
# <http://www.gnu.org/licenses/>.

import ast

# Restrict import
__all__ = ['translate']

def translate(source):
    """Return a string containing the Dafny translation of the Python source
    code in string source.
    """

    # Create the abstract syntax tree from the source code.
    tree = ast.parse(source)

    dafny_translator = DafnyTranslator()
    return translator.initiate_translate(tree)


class DafnyTranslator(ast.NodeVisitor):
    """Translate Python code into Dafny code."""

    def __init__(self):
        self.src = ""  # Dafny source code to be built upon.
        self.indent = 0  # Scope indentation level.

    def initiate_translate(self, node):
        """Call the visit function, which adds the Python source code from the
        abstract syntax tree beginning in node to this DafnyTranslator's
        source attribute. Return this DafnyTranslator's source attribute.
        """

        self.visit(node)
        return self.src

    def _indent(self, line):
        """Return an appropriately indented version of this line.
        """

        return "%s%s" % (" " * self.indent, line)

    def _render_block(self, body):
        """Render a block of code with the correct indentation.
        """
        self.indent += 2
        for stmt in body:
            self.visit(stmt)
        self.indent -= 2

    def visit_FunctionDef(self, defn):
        """Append the Dafny translation of the tree beginning at node defn to
        this DafnyTranslator's src attribute.
        """

        func_translator = FunctionTranslator()
        self.src += func_translator.initiate_translation(defn)

    def visit_Expr(self, expr):
        """Append expr, which is expected to be the preconditions,
        postconditions, and the docstring, to this FunctionTranslator's src
        attribute.
        """
        L = expr.value.s.split("\n")

        docstring = '\n'


    def visit_If(self, if_):
        """Append the Dafny translation of the tree beginning at node if_ to
        this DafnyTranslator's src attribute.

        This function translates an if statement and calls the visit function
        on its body.
        """

        self.src += self._indent("if ")
        self.visit(if_.test)
        self.src += " then\n"
        self._render_block(if_.body)
        self.src += self._indent()  # Check if anything needs to be appended.

    def visit_Compare(self, compare):
        """Append the Dafny translation of the tree beginning at node compare to
        this DafnyTranslator's src attribute.

        This function translates a compare statement, calling the visit
        function on its children.
        """
        self.visit(compare.left)
        self.src += " "
        self.visit(compare.ops[0])
        self.src += " "
        self.visit(compare.comparators[0])

    def visit_Return(self, ret):
        """Append the Dafny translation of the tree beginning at node ret to
        this DafnyTranslator's src attribute.

        This function translates a return statement, calling the visit function
        on the return expression.
        """

        if ret.value:
            # This function returns something.
            self.returns = True

            self.src += "\n"

            self.src += self._indent("result = ")  # Create the return variable
            self.visit(ret.value)
            self.src += "\n"

            self.src += self._indent("return")




class FunctionTranslator(DafnyTranslator):
    """Translate a Python function into Dafny code."""

    # Override the initialisation method.
    def __init__(self):
        self.func_name = "" # Name of the function.
        self.args = "" # Argument list in Dafny format.
        self.return_value = "" # Name of the return value.
        self.return_type = "" # Type of the return value.

        self.pre = "" # Boolean precondition.
        self.post = "" # Boolean postcondition.
        self.frame = ""  # Comma delimited string of modified arguments.
        self.rank = ""  # Comma delimited string of decreasing arguments.

    def initiate_translation(defn):
        """Translate the Python source code contained in the tree rooted in
        node defn, which is expected to be a function definition, into Dafny
        source code.

        This method overrides the initiate_translation method of the parent
        class DafnyTranslator.
        """

        # Create the function name string.
        funcname = defn.name
        funcname.replace('_', '')
        funcname.capitalize()

        # Create the argument string, including parentheses.
        args = '('
        for arg in defn.args.args:
            args + arg.arg  # Append the argument name.
            args + ': '
            args + arg.annotation.id  # Append the argument type.
            args + ', '
        args = args[:-2]  # Truncate the last comma and space.
        args + ')'

        # Create the first line of the function definition.
        firstline = "method " + funcname + args
        self.src += self._indent(firstline)

        # Check if a return specification needs to be inserted into the
        # Dafny specification.
        if self.returns == True:

            self.src += " returns (result: "

            # Get the type of the return value.
            # self.src += defn.returns.id
            self.src += ")\n"

            # Set this DafnyTranslator's returns attribute to the default.
            self.returns = False

        # Function opening brace.
        self.src += "{"
        # Proceed with the body of the function.
        self._render_block(defn.body)

        self.src += self._indent("}\n")

    def visit_Expr(self, expr):
        """Append expr, which is expected to be the preconditions,
        postconditions, and the docstring, to this FunctionTranslator's src
        attribute.
        """
        L = expr.value.s.split("\n")

        docstring = '\n'

        for line in L:
            if line.startswith("Pre"):
                # pre = _format_precondition(L[0].replace("Pre: ", "")) + '\n'
                pass
            elif line.startswith("Post"):
                # post = _format_postcondition(L[1].replace("Post: ", "")) + '\n'
                pass
            else:
                docstring += '// ' + line

        # Get rid of the last comment designation.
        docstring = docstring.rstrip("\n /")

        pre = ''
        post = ''

        self.src += pre + post + docstring

    def _format_precondition(s):
        """Return s in the form of a Dafny precondition.
        """

        return s

    def _format_postcondition(s):
        """Return s in the form of a Dafny postcondition.
        """

        return s


