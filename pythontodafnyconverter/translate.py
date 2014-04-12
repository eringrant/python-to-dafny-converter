import ast

class DafnyTranslator(ast.NodeVisitor):
    """Translate a Python function into a dafny function."""

    def __init__(self):
        self.src = ""  # Dafny source code to be built upon.
        self.indent = 0  # Indentation level to identify scope.

    def translate(self, node)
    """Call the visit function, which adds the Python source code from node to
    this DafnyTranslator's source attribute. Return this DafnyTranslator's
    source attribute.
    """

        self.visit(node)
        return self.src

    def _indent(self, line):
    # Used to help indent the code.
        return "%s%s" % (" " * self._indent, line)

    def render_block(self, body):
    """Render a block of code with the correct indentation.
    """
        self._indent += 2
        for stmt in body:
            self.visit(stmt)
        self._indent -= 2

    def visit_FunctionDef(self, defn):
        """Append the Dafny translation of the tree beginning at node defn to
        this DafnyTranslator's src attribute.
        """

        # Create the argument string, including parentheses.
        args = '('
        for arg in defn.args:
            args.append(arg)
            args.append(',')
        args.append(')')

        # Create the first line of the function definition.
        firstline = "method " + funcname + args + " returns " + returns + "\n"
        self.src += self._indent(firstline)


    def _type_list(docstring):
    """(str) -> list
    Return the user-defined argument-type and return-type lists from docstring.
    """
        (arg_type_str, __, ret_type_str) = docstring.partition("->")

        # Strip the strings of extra characters, whitespace and parentheses.
        arg_type_str.strip(' ()')

        i = ret_type_str.find()
        ret_type_str = ret_type_str[:i+1]
        ret_type_str.strip(' ()')


    def _arg_list(arglist):
    """(list) -> str
    Return the Dafny representation of the arguments in arglist, including
    parentheses.

    A Dafny argument list specifies the types of the arguments, and has the
    following format: (variable1: type1, variable2: type2).
    """

        dafny_arglist = "("

        for arg in arglist:



