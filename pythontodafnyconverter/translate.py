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


# Constants representing Dafny operator syntax.
BOOLOP_SYMBOLS = {
        'And' : '&&',
        'Or' : '||',
}

OPERATOR_SYMBOLS = {
        'Add' : '+',
        'Sub' : '-',
        'Mult' : '*',
        'Div' : '/',
        'Mod' : '%',
        'Pow' : '^',  #TODO: Check if this is the appropriate operator.
        'LShift' : '<<',
        'RShift' : '>>',
        'BitOr' : '',  #TODO: Determine Dafny symbol.
        'BitXor' : '',  #TODO: Determine Dafny symbol.
        'BitAnd' : '',  #TODO: Determine Dafny symbol.
        'FloorDiv' : '',  #TODO: Determine Dafny symbol.
}

UNARYOP_SYMBOLS = {
        'Invert' : '',  #TODO: Determine Dafny symbol.
        'Not' : '',  #TODO: Determine Dafny symbol.
        'UAdd' : '',  #TODO: Determine Dafny symbol.
        'USub' : '',  #TODO: Determine Dafny symbol.
}

CMPOP_SYMBOLS = {
        'Eq' : '==',
        'NotEq' : '!=',
        'Lt' : '<',
        'LtE' : '<=',
        'Gt' : '>',
        'GtE' : '>=',
        'Is' : '',  #TODO: Determine Dafny symbol.
        'IsNot' : '',  #TODO: Determine Dafny symbol.
        'In' : '',  #TODO: Determine Dafny symbol.
        'NotIn' : '',  #TODO: Determine Dafny symbol.
}


class Error(Exception):
    """Base class for exceptions in this module."""

    pass

class NoAttributeError(Error):
    """Exception raised when no Dafny source code exists.

    Attributes:
        attr -- attribute which is missing
        msg -- explanation of the error
    """

## Override.
#    def __init__(self, attr, msg):
#        self.attr = attr
#        self.msg = msg


class NoPreconditionError(NoAttributeError):
    """Exception raised when no precondition is defined."""

    pass


class NoPostconditionError(NoAttributeError):
    """Exception raised when no postcondition is defined."""

    pass

class NoDocstringError(NoAttributeError):
    """Exception raised when no docstring is defined."""

    pass

class NoInvariantError(NoAttributeError):
    """Exception raised when no invariant is defined."""

    pass

class ForLoopError(Error):
    """Exception raised when a for loop is encountered."""

    pass

class NoBodyError(NoAttributeError):
    """Exception raised when no body is defined."""

    pass


class ExtraCommentError(Error):
    """Exception raised when an extra comment can't be parsed."""

    pass

def translate(source):
    """Return a string containing the Dafny translation of the Python source
    code in string source.
    """
    assert isinstance(source, str)
    # Create the abstract syntax tree from the source code.
    tree = ast.parse(source)

    dafny_translator = DafnyTranslator()
    return dafny_translator.initiate_translation(tree)


class DafnyTranslator(ast.NodeVisitor):
    """Translate Python code into Dafny code."""

    def __init__(self):
        self.src = None  # Final Dafny source code.
        self.body = []  # Accumulator for translated material.
        self.indent = 0  # Indentation scope level.
        self.if_scope = 0  # Level of embedding in an if statement.

    def append(item):
        """Add item to this DafnyTranslator."""
        assert isinstance(item, str)
        self.body.append(item)

    def get_source_code(self):
        """Return the source code accumulated by this DanfyTranslator."""
        return "".join(self.body)

    def initiate_translation(self, node):
        """Add the Dafny translation of the Python source code from the
        abstract syntax tree beginning in node to this DafnyTranslator's
        source attribute. Return this DafnyTranslator's source attribute.
        """
        print(ast.dump(node))
        s = self.visit(node)
        print(self.body)
        print(self.src) #TODO
        assert isinstance(s, str)
        self.append(s)
        return self.get_source_code()

    def _indent(self, line):
        """Return an appropriately indented version of this line.
        """

        return "%s%s" % (" " * self.indent, line)

    def _render_block(self, body):
        """Render a block of code with the correct indentation.
        """
        s = ""
        self.indent += 2
        for stmt in body:
            try:
                s += self.visit(stmt)
            except TypeError:
                raise NoBodyError
        self.indent -= 2
        return s

    def visit_FunctionDef(self, defn):
        """Append the Dafny translation of the tree beginning at node defn to
        this DafnyTranslator's body attribute.
        """

        if "function" in defn.name:
            translator = FunctionTranslator(self.indent)
            return translator.initiate_translation(defn)
        elif "method" in defn.name:
            translator = MethodTranslator(self.indent)
            return translator.initiate_translation(defn)
        else:
#            raise NoTypeSpecifiedError  #TODO: create exception
            pass

    def visit_For(self, for_):
        """Raise a ForLoopError.
        """
#        raise ForLoopError
        pass
        # TODO: integrate for loops as while loops

    def visit_While(self, while_):
        """Append the Dafny translation of the tree beginning at while_ to
        this DafnyTranslator's body attribute.
        """

        loop_translator = LoopTranslator(self.indent)
        return loop_translator.initiate_translation(while_)

    def visit_Expr(self, expr):
        """Append expr, which is expected to be a simple comment, to this
        FunctionTranslator's src attribute.
        """
        # TODO: Check whether the parser remove the comment specifiers.

    def visit_If(self, if_):
        """Append the Dafny translation of the tree beginning at node if_ to
        this DafnyTranslator's src attribute.

        This function translates an if statement and calls the visit function
        on its body.
        """

        s = self._indent("if ")
        s += self.visit(if_.test)
        s += "{\n"
        s += if_.body
        s += self._indent("}\n")
        return s

#TODO: implement a generator in order to exhaust the if node

    def visit_Compare(self, compare):
        """Append the Dafny translation of the tree beginning at node compare to
        this DafnyTranslator's src attribute.

        This function translates a compare statement, calling the visit
        function on its children.
        """
        s = self.visit(compare.left)
        s += " "
        s += compare.ops[0]
        s += " "
        s += compare.comparators[0]
        return s

    def visit_Assign(self, assign):
        """Append the Dafny translation of assign to this
        FunctionTranslator's body attribute.
        """
        s = self.visit(assign.value)
        s += " := "
        s += self.visit(assign.targets)  #TODO: check that produces correct output
        return s

    def visit_BinOp(self, bin_op):
        s = self.visit(bin_op.left)
        s += OPERATOR_SYMBOLS[bin_op.op]
        s += self.visit(bin_op.right)  #TODO: check that produces correct output
        return s

    def visit_UnaryOp(self, unary_op):
        s = UNARYOP_SYMBOLS[unary_op.op]
        s += self.visit(unary_op.operand)  #TODO: check that produces correct output
        return s

    def visit_If(self, if_):
        if self.if_scope > 0
        s = "if "
        s +=

    def visit_BoolOp(self, bool_op):
        s = BOOLOP_SYMBOLS[bool_op.op]
        s += self.visit(bool_op.values)
        return s

class MethodTranslator(DafnyTranslator):
    """Translate a Python function into Dafny code."""

    # Override the initialisation method.
    def __init__(self, indent):
        super().__init__()

        self.indent = indent  # Same scope as parent's current level.

        self.func_name = None  # Name of the function.

        self.args = {}  # Arguments dict (keys: name; values: type).
        self.returns = {}  # Return values dict (keys: name; values: types).

        self.pre = None  # Boolean precondition.
        self.post = None  # Boolean postcondition.
        self.frame = None  # Comma delimited string of modified arguments.
        self.rank = None  # Comma delimited string of decreasing arguments.

        self.docstring = None  # The docstring of the function.
        self.function_body = None  # The body of the function.

    def initiate_translation(self, defn):
        """Translate the Python source code contained in the tree rooted in
        node defn, which is expected to be a function definition, into Dafny
        source code.

        This method overrides the initiate_translation method of the parent
        class DafnyTranslator.
        """
        self.set_function_name(defn)
        self.set_arguments(defn)

        # Proceed with the body of the function.
        self.body = self._render_block(defn.body)

        return self.compile_body()

    def compile_body(self):
        if isinstance(self, MethodTranslator):
            s = "method  "
        elif isinstance(self, FunctionTranslator):
            s = "function  "
        else:
            print("Wrong class reached function def translation.") #TODO

        try:
            s += self.func_name
        except TypeError:
#            raise NoFunctionNameError
            pass

        try:
            s += "(" + self.get_args + ")"
        except TypeError:
#            raise NoArgumentsError
            pass

        if isinstance(self, MethodTranslator):
            try:
                s += " returns (" + self.get_returns + ")"
            except TypeError:
                pass  # Append nothing if there was no return value.
            s += "\n"
        elif isinstance(self, FunctionTranslator):
            try:
                s += ": " + self.get_returns
            except TypeError:
                pass  # Append nothing if there was no return value.
            s += "\n"
        else:
            print("Wrong class reached function def translation.") #TODO

        try:
            s += self.pre
        except TypeError:
#            raise NoPreconditionsError
            pass
        else:
            s += ";\n"

        try:
            s += self.post
        except TypeError:
#            raise NoPostconditionsError
            pass
        else:
            s += ";\n"

        try:
            s += self.frame
        except TypeError:
#            raise NoFrameSetError
            pass
        else:
            s += ";\n"

        # Append the rank set.
        try:
            s += self.rank
        except TypeError:
#            raise NoRankSetError
            pass
        else:
            s += ";\n"

        # Visit the body of the function.
        s += "{\n"
        s += body
        s += "\n}"

        return s

    def set_function_name(self, defn):
        """Set this Dafny Translator's function name attribute to the name of
        the function corresponding to this defn node.
        """
        self.func_name = defn.name.replace('_', '').capitalize()

    def set_arguments(self, defn):
        """Append to this Dafny Translator's arguments attribute the names and
        types of the arguments of the function corresponding to this defn node.
        """
        for arg in defn.args.args:
            self.args[arg.arg] = arg.annotation.id

    def get_args(self):
        """Return the argument specification accumulated by this
        DafnyTranslator, in Dafny format, if any arguments exist; otherwise,
        return None.
        """
        L = []
        for arg in self.args:
            L.append(arg + ": " + self.args[arg])
        if L:
            return ", ".join(L)
        else:
            return None

    def get_returns(self):
        """Return the return values specification accumulated by this
        DafnyTranslator, in Dafny format, if any values exist; otherwise,
        return None.
        """
        L = []
        for value in self.returns:
            L.append(value + ": " + self.returns[value])
        if L:
            return ", ".join(L)
        else:
            return None


    def visit_Expr(self, expr):
        """Parse the string in expr, which is expected to be function
        preconditions, postconditions, the frame set and the rank set,
        and the docstring, and add to this FunctionTranslator's appropriate
        attribute.
        """

        s = expr.value.s.strip()
        L = s.split("\n")

        for line in L:
            line = line.strip()
            if line.startswith("var"):
                self.set_returns(self.remove_spec(line))
            elif line.startswith("pre"):
                self.set_precondition(self.remove_spec(line))
            elif line.startswith("post"):
                self.set_postcondition(self.remove_spec(line))
            elif line.startswith("mod"):
                self.set_frame(self.remove_spec(line))
            elif line.startswith("dec"):
                self.set_rank(self.remove_spec(line))
            else:
                self.set_docstring(self.remove_spec(line))

    def remove_spec(self, line):
        """Return line truncated to the string beyond the first colon."""
        i = line.find(":")
        line = line [i+1:]
        return line.strip()

    def set_returns(self, line):
        """Set this FunctionTranslator's return specifications according to the
        information contained in line.
        """
        if ";" in line:
            line.replace(";", ",")
        L = line.split(",")
        for item in L:
            pair = item.split(":")
            if not pair[0] in self.args:
                self.returns[pair[0]] = pair[1].lower().strip()

    def set_precondition(self, line):
        """Set this FunctionTranslator's precondition to the correctly
        indented, Dafny formatted version of line."""
        self.pre = "  requires " + line + ";\n"

    def set_postcondition(self, line):
        """Set this FunctionTranslator's postcondition to the correctly
        indented, Dafny formatted version of line."""
        self.post = "  ensures " + line + ";\n"

    def set_frame(self, line):
        """Set this FunctionTranslator's frame set to the correctly
        indented, Dafny formatted version of line."""
        self.frame = "  modifies " + line + ";\n"

    def set_rank(self, line):
        """Set this FunctionTranslator's rank set to the correctly
        indented, Dafny formatted version of line."""
        self.rank = "  decreases " + line + ";\n"

    def set_docstring(self, line):
        """Add line to this DafnyTranslator's docstring."""
        try:
            self.docstring += "\n// " + line
        except TypeError:
            self.docstring = "// " + line

    def visit_Return(self, ret):
        """Return the expression following the return statement, if applicable.

        If the expression is a single value
        """


        self.body += self._indent("result := ")
        self.visit(ret.value)

#TODO: for multiple returns (i.e., tuples), think about using a dictionary

class FunctionTranslator(MethodTranslator):
    """Translate a Python function into Dafny function code."""

    # Override the initialisation method.
    def __init__(self, indent):
        super().__init__()

        self.returns = None
        # A function in Dafny only has specification for return value type.


    def initiate_translation(self, defn):
        """Translate the Python source code contained in the tree rooted in
        node defn, which is expected to be a function definition, into Dafny
        source code.

        This method overrides the initiate_translation method of the parent
        class DafnyTranslator.
        """
        self.set_function_name(defn)
        self.set_arguments(defn)
        self.set_returns(defn)

    def set_returns(self, defn):
        """Set this FunctionTranslator's return type specifications according to the
        information contained in node defn.

        Override from parent MethodTranslator.
        """
        assert isinstance(defn, FunctionDef)
        self.returns = defn.returns.id
        assert isinstance(self.returns, str)

    def visit_Expr(self, expr):
        """Parse the string in expr, which is expected to be function
        preconditions, postconditions, the frame set and the rank set,
        and the docstring, and add to this FunctionTranslator's appropriate
        attribute.
        """
        s = expr.value.s.strip()
        L = s.split("\n")

        for line in L:
            line = line.strip()
            if line.startswith("pre"):
                self.set_precondition(self.remove_spec(line))
            elif line.startswith("post"):
                self.set_postcondition(self.remove_spec(line))
            elif line.startswith("mod"):
                self.set_frame(self.remove_spec(line))
            elif line.startswith("dec"):
                self.set_rank(self.remove_spec(line))
            else:
                self.set_docstring(self.remove_spec(line))

class LoopTranslator(FunctionTranslator):

    # Override the initialisation method.
    def __init__(self, indent):
        super().__init__(indent)

        self.invariant = None  # The loop invariant.

    def visit_Expr(self, expr):
        """Parse the string in expr, which is expected to be the loop
        invariant, and add to this LoopTranslator's invariant attribute.
        """

        expression = expr.value.s.strip()
        L = expression.split("\n")

        for line in L:
            line = line.strip()
            if line.startswith("inv"):
                i = line.find(":")
                line = line[i+1:]
                line = line.strip()
                self.invariant = line
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
#TODO:          raise ExtraCommentError
                pass

