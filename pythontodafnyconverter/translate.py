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


class Error(Exception):
    """Base class for exceptions in this module."""

    pass

class NoAttributeError(Error):
    """Exception raised when no Dafny source code exists.

    Attributes:
        attr -- attribute which is missing
        msg -- explanation of the error
    """

    # Override.
    def __init__(self, attr, msg):
        self.attr = attr
        self.msg = msg


class NoPreconditionError(NoAttributeError):
    """Exception raised when no precondition is defined."""

    pass


class NoPostconditionError(NoAttributeError):
    """Exception raised when no postcondition is defined."""

    pass

class ForLoopError(Error):
    """Exception raised when a for loop is encountered."""

def translate(source):
    """Return a string containing the Dafny translation of the Python source
    code in string source.
    """

    # Create the abstract syntax tree from the source code.
    tree = ast.parse(source)

    dafny_translator = DafnyTranslator()
    return dafny_translator.initiate_translate(tree)


class DafnyTranslator(ast.NodeVisitor):
    """Translate Python code into Dafny code."""

    def __init__(self):
        self.src = Nonce # Dafny source code to be built upon.
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
        for stmt in body: self.visit(stmt)
        self.indent -= 2

    def visit_FunctionDef(self, defn):
        """Append the Dafny translation of the tree beginning at node defn to
        this DafnyTranslator's src attribute.
        """

        func_translator = FunctionTranslator()
        self.src += func_translator.initiate_translation(defn)

    def visit_For(self, for_):
        """Raise a ForLoopError.
        """
        raise ForLoopError

    def visit_While(self, while_):
        """Append the Dafny translation of the tree beginning at while_ to
        this DafnyTranslator's src attribute.
        """

        loop_translator = LoopTranslator()
        self.src += loop_translator.initiate_translation(while_)

    def visit_Expr(self, expr):
        """Append expr, which is expected to be a simple comment, to this
        FunctionTranslator's src attribute.
        """
        # Check whether the parser remove the comment specifiers.

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
#   what does this mean

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




class FunctionTranslator(DafnyTranslator):
    """Translate a Python function into Dafny code."""

    # Override the initialisation method.
    def __init__(self):
        super().__init__()

        self.indent = super().indent  # Same scope as parent's current level.

        self.func_name = None  # Name of the function.
        self.args = None  # Argument list in Dafny format.
        # self.return_value = None  # Name of the return value. Not implemented.
        self.return_type = None  # Type of the return value.

        self.pre = None  # Boolean precondition.
        self.post = None  # Boolean postcondition.
        self.frame = None  # Comma delimited string of modified arguments.
        self.rank = None  # Comma delimited string of decreasing arguments.

        self.docstring = None  # The docstring of the function, with newlines.
        self.body = None  # The body of the function.

    def initiate_translation(self, defn):
        """Translate the Python source code contained in the tree rooted in
        node defn, which is expected to be a function definition, into Dafny
        source code.

        This method overrides the initiate_translation method of the parent
        class DafnyTranslator.
        """

        # Access the function name string.
        self.func_name = defn.name
        self.func_name = self.func_name.replace('_', '')
        self.func_name = self.func_name.capitalize()

        # ADD CODE LATER TO CAPITALIZE THE WORD AFTER THE UNDERSCORE

        # Create the argument specification, including parentheses.
        self.args = '('
        for arg in defn.args.args:
            args + arg.arg  # Append the argument name.
            args + ': '
            args + arg.annotation.id  # Append the argument type.
            args + ', '
        self.args = self.args[:-2]  # Truncate the last comma and space.
        self.args += ')'

        # Proceed with the body of the function.
        self._render_block(defn.body)


        # Put everything together by appending to this FunctionTranslator's src
        # attribute. At this point, the src attribute is expected to be None.

        # Append the function name and type declarations.
        self.src = "method "
        self.src += self.func_name
        self.src += self.args
        self.src += " returns (result: "
        self.src += self.return_type
        self.src += ")\n"

        # Append the docstring.
        docstring = "// "
        try:
            self.docstring.split("\n")
        except TypeError:
            raise NoDocstringError
        else:
            for line in docstring:
                docstring += line += "\n//"
            docstring = docstring[:-2] # Truncate the extra newline and slashes.
            self.src += docstring

        # Append the precondition.
        pre = "  requires "
        try:
            pre = pre + self.pre
        except TypeError:
            raise NoPreconditionError
        else:
            pre + ";\n"
            self.src += pre

        # Append the postcondition.
        pre = "  ensures "
        try:
            pre = pre + self.pre
        except TypeError:
            raise NoPostconditionError
        else:
            pre + ";\n"
            self.src += pre

        # Append the frame set.
        frame = "  modifies "
        try:
            frame = frame + self.frame
        except TypeError:
            raise NoFrameSetError
        else:
            frame + ";\n"
            self.src += frame

        # Append the rank set.
        pre = "  decreases "
        try:
            rank = rank + self.rank
        except TypeError:
            raise NoRankSetError
        else:
            rank + ";\n"
            self.src += rank

        # Visit the body of the function.
        self.src += "{\n"
        self.visit(defn.body)
        self.src += "\n}"

        return self.src

    def visit_Expr(self, expr):
        """Parse the string in expr, which is expected to be function
        preconditions, postconditions, the frame set and the rank set,
        and the docstring, and add to this FunctionTranslator's appropriate
        attribute.
        """

        L = expr.value.s.split("\n")

        docstring = '//'

        for line in L:
            line = line.strip()
            if line.startswith("pre"):
                i = line.find(":")
                line = line[i+1:]
                line = line.strip()
                self.pre = line
            elif line.startswith("post"):
                i = line.find(":")
                line = line[i+1:]
                line = line.strip()
                self.post = line
            elif line.startswith("mod"):
                i = line.find(":")
                line = line[i+1:]
                line = line.strip()
                self.frame = line
            elif line.startswith("dec"):
                i = line.find(":")
                line = line[i+1:]
                line = line.strip()
                self.rank = line
            else:
                docstring += line + "//\n"

        docstring = docstring.rstrip("\n /")
        if len(docstring) > 0:
            self.docstring

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


class LoopTranslator(FunctionTranslator):

    # Override the initialisation method.
    def __init__(self):
        super().__init__()

        self.indent = super().indent  # Same scope as parent's current level.

        self.invariant = None  # The loop invariant.
        self.body = None  # The body of the function.


