# pylint: disable=W0108,R0902,R0913,R0914,too-many-lines,too-many-statements,too-many-nested-blocks
"""
TW Forth Language Executor
==========================

Implements TW Forth, an educational variant of the Forth stack-based programming
language for the Time_Warp IDE, emphasizing postfix notation and stack manipulation.

Language Features:
- Stack manipulation: DUP, DROP, SWAP, ROT, OVER, NIP, TUCK
- Arithmetic: +, -, *, /, MOD, /MOD, MIN, MAX, ABS, NEGATE
- Comparison: =, <, >, <=, >=, 0=, 0<, 0>
- Bitwise operations: AND, OR, XOR, INVERT
- Control structures: IF/THEN/ELSE, BEGIN/UNTIL, BEGIN/WHILE/REPEAT, DO/LOOP
- Word definition: : (colon) to define new words, ; (semicolon) to end
- Variables: VARIABLE to create named storage locations
- Constants: CONSTANT to define named values
- Comments: ( for line comments, \\ for end-of-line comments
- I/O: . (dot) to print, .S to show stack, CR for newline, EMIT for characters
- Strings: S" for string literals
- Math functions: SIN, COS, TAN, SQRT, LOG, EXP

GFORTH EXTENSIONS:
- Locals: { local1 local2 } for local variables in definitions
- Objects: Object-oriented programming with classes and methods
- Floating point: Enhanced floating point operations (F+, F-, F*, F/)
- File access: File I/O operations (OPEN-FILE, READ-FILE, WRITE-FILE, CLOSE-FILE)
- Memory allocation: ALLOCATE, FREE, RESIZE for dynamic memory
- Exception handling: TRY...THROW...CATCH for error handling
- Structures: C-like structures with FIELD and STRUCT
- Value: Mutable constants with TO for reassignment
- Extended numerics: Double precision operations (D+, D-, D*, D/)
- String handling: Enhanced string operations (COMPARE, SEARCH, etc.)

The executor provides a stack-based programming environment where operations
work on data items pushed onto and popped from a parameter stack.
"""

import re
import math

# pylint: disable=too-many-lines,too-many-instance-attributes,W0108,W0718,R1705,R0911,R0912,R0903


class TwForthExecutor:
    """Handles TW Forth language command execution"""

    def __init__(self, interpreter):
        """Initialize with reference to main interpreter"""
        self.interpreter = interpreter
        self.data_stack = []  # Main data stack
        self.return_stack = []  # Return stack for control structures
        self.float_stack = []  # Floating point stack
        self.dictionary = {}  # User-defined words
        self.variables = {}  # Variables
        self.constants = {}  # Constants
        self.values = {}  # Mutable constants (VALUE/TO)
        self.locals = {}  # Local variables in current definition
        self.objects = {}  # Object definitions
        self.structures = {}  # Structure definitions
        self.files = {}  # Open file handles
        self.memory_blocks = {}  # Allocated memory blocks
        self.compiling = False  # Are we in compile mode?
        self.current_word = None  # Word being defined
        self.word_definition = []  # Words being compiled
        self.if_depth = 0  # Nested IF depth
        self.loop_depth = 0  # Nested loop depth
        self.local_depth = 0  # Local variable depth
        self.exception_handlers = []  # Exception handling stack
        self.next_file_id = 0  # For file handle management
        self.next_memory_id = 0  # For memory block management
        # Temporary flags when following tokens act as names
        self.expecting_variable_name = False
        self.pending_variable_name = None
        self.expecting_constant_name = False
        self.pending_constant_value = None

        # Initialize built-in words
        self._init_builtin_words()

    def _init_builtin_words(self):  # pylint: disable=unnecessary-lambda
        """Initialize built-in Forth words"""
        self.dictionary.update(
            {
                # Stack manipulation
                "DUP": lambda: self._dup(),
                "DROP": lambda: self._drop(),
                "SWAP": lambda: self._swap(),
                "OVER": lambda: self._over(),
                "ROT": lambda: self._rot(),
                "NIP": lambda: self._nip(),
                "TUCK": lambda: self._tuck(),
                # Arithmetic
                "+": lambda: self._add(),
                "-": lambda: self._sub(),
                "*": lambda: self._mul(),
                "/": lambda: self._div(),
                "MOD": lambda: self._mod(),
                "NEGATE": lambda: self._negate(),
                "ABS": lambda: self._abs(),
                "1+": lambda: self._one_plus(),
                "1-": lambda: self._one_minus(),
                "2+": lambda: self._two_plus(),
                "2-": lambda: self._two_minus(),
                "2*": lambda: self._two_times(),
                "2/": lambda: self._two_divide(),
                "MIN": lambda: self._min(),
                "MAX": lambda: self._max(),
                # Comparison
                "=": lambda: self._equal(),
                "<": lambda: self._less(),
                ">": lambda: self._greater(),
                "<=": lambda: self._less_equal(),
                ">=": lambda: self._greater_equal(),
                "<>": lambda: self._not_equal(),
                # Logic
                "AND": lambda: self._and(),
                "OR": lambda: self._or(),
                "XOR": lambda: self._xor(),
                "INVERT": lambda: self._invert(),
                # I/O
                ".": lambda: self._dot(),
                ".S": lambda: self._dot_s(),
                '."': lambda: self._dot_quote(),
                "CR": lambda: self._cr(),
                "EMIT": lambda: self._emit(),
                "SPACES": lambda: self._spaces(),
                # Math functions
                "SIN": lambda: self._sin(),
                "COS": lambda: self._cos(),
                "TAN": lambda: self._tan(),
                "SQRT": lambda: self._sqrt(),
                "LOG": lambda: self._log(),
                "EXP": lambda: self._exp(),
                # Stack queries
                "DEPTH": lambda: self._depth(),
                "PICK": lambda: self._pick(),
                "ROLL": lambda: self._roll(),
                # Constants
                "TRUE": lambda: self.data_stack.append(-1),
                "FALSE": lambda: self.data_stack.append(0),
                "PI": lambda: self.data_stack.append(math.pi),
                "E": lambda: self.data_stack.append(math.e),
                # Gforth extensions
                # Floating point operations
                "F+": lambda: self._f_add(),
                "F-": lambda: self._f_sub(),
                "F*": lambda: self._f_mul(),
                "F/": lambda: self._f_div(),
                "F.": lambda: self._f_dot(),
                "F@": lambda: self._f_fetch(),
                "F!": lambda: self._f_store(),
                "FDUP": lambda: self._f_dup(),
                "FDROP": lambda: self._f_drop(),
                "FSWAP": lambda: self._f_swap(),
                # Double precision operations
                "D+": lambda: self._d_add(),
                "D-": lambda: self._d_sub(),
                "D*": lambda: self._d_mul(),
                "D/": lambda: self._d_div(),
                "D.": lambda: self._d_dot(),
                "D@": lambda: self._d_fetch(),
                "D!": lambda: self._d_store(),
                # Loop index
                "I": lambda: self._i(),
                # Memory allocation
                "ALLOCATE": lambda: self._allocate(),
                "FREE": lambda: self._free(),
                "RESIZE": lambda: self._resize(),
                # File operations
                "OPEN-FILE": lambda: self._open_file(),
                "CLOSE-FILE": lambda: self._close_file(),
                "READ-FILE": lambda: self._read_file(),
                "WRITE-FILE": lambda: self._write_file(),
                "FILE-POSITION": lambda: self._file_position(),
                "REPOSITION-FILE": lambda: self._reposition_file(),
                # String operations
                "COMPARE": lambda: self._compare(),
                "SEARCH": lambda: self._search(),
                "SLITERAL": lambda: self._sliteral(),
                # Exception handling
                "TRY": lambda: self._try(),
                "THROW": lambda: self._throw(),
                "CATCH": lambda: self._catch(),
                # Value (mutable constants)
                "VALUE": lambda: self._value(),
                "TO": lambda: self._to(),
                # Structure operations
                "STRUCT": lambda: self._struct(),
                "FIELD": lambda: self._field(),
                "END-STRUCT": lambda: self._end_struct(),
                # Object operations
                "OBJECT": lambda: self._object(),
                "METHOD": lambda: self._method(),
                "END-OBJECT": lambda: self._end_object(),
                "NEW": lambda: self._new(),
                "SEND": lambda: self._send(),
            }
        )

    def execute_command(self, command):
        """Execute a Forth command and return the result"""
        try:
            command = command.strip()
            if not command:
                return "continue"

            # Split command into words
            words = self._tokenize(command)

            for word in words:
                if not self._execute_word(word):
                    return "continue"

            # If we're compiling and haven't seen the semicolon yet,
            # return a special value to indicate continuation needed
            if self.compiling:
                return "forth_compiling"

            return "continue"

        except Exception as e:
            self.interpreter.debug_output(f"Forth command error: {e}")
            return "continue"

    def _tokenize(self, command):
        """Tokenize Forth command into words"""
        # Handle comments first
        # Remove backslash comments (from \ to end of line)
        if command.strip().startswith("\\"):
            return []  # Entire line is a comment
        command = re.sub(r"\\.*$", "", command)
        # Remove parenthesis comments
        command = re.sub(r"\(.*?\)", "", command)  # Remove ( comments )

        # Handle .\" strings specially
        command = re.sub(r"\.\"([^\"]*?)\"", r'."\1"', command)

        # Split on whitespace, keeping quoted strings together
        tokens = []
        current_token = ""
        in_string = False

        for char in command:
            if char == '"' and not in_string:
                in_string = True
                current_token += char
            elif char == '"' and in_string:
                in_string = False
                current_token += char
                tokens.append(current_token)
                current_token = ""
            elif char.isspace() and not in_string:
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            else:
                current_token += char

        if current_token:
            tokens.append(current_token)

        return tokens

    def _execute_word(self, word):
        """Execute a single Forth word"""
        try:
            # Handle tokens that are expected to be names for VARIABLE/CONSTANT
            if self.expecting_variable_name:
                name = word
                # Create variable storage with default 0
                self.variables[name] = 0
                # Add execution hook so using variable pushes reference
                self.dictionary[name] = lambda n=name: self.data_stack.append(
                    {"type": "var", "name": n}
                )
                self.expecting_variable_name = False
                self.pending_variable_name = None
                self.interpreter.log_output(f"Variable declared: {name}")
                return True

            if self.expecting_constant_name:
                name = word
                self.constants[name] = self.pending_constant_value
                # Add a word so constant name pushes constant value
                self.dictionary[name] = (
                    lambda v=self.pending_constant_value: self.data_stack.append(v)
                )
                self.expecting_constant_name = False
                self.pending_constant_value = None
                self.interpreter.log_output(f"Constant declared: {name}")
                return True

            # Handle numbers (including floating point)
            if self._is_number(word):
                if self.compiling:
                    self.word_definition.append(word)
                else:
                    if "." in word and word.count(".") == 1:
                        # Floating point number
                        self.float_stack.append(self._parse_number(word))
                    else:
                        # Integer
                        self.data_stack.append(self._parse_number(word))
                return True

            # Handle strings
            if word.startswith('"') and word.endswith('"'):
                if self.compiling:
                    self.word_definition.append(word)
                else:
                    self.data_stack.append(word[1:-1])  # Remove quotes
                return True

            # Handle locals definition
            if word == "{":
                return self._handle_locals_start()
            elif word == "}":
                return self._handle_locals_end()

            # Handle word definition start
            if word == ":":
                self.compiling = True
                self.word_definition = []
                self.current_word = None
                self.locals = {}  # Reset locals for new definition
                return True

            # If compiling and we don't have a word name yet, this is the word name
            if self.compiling and self.current_word is None:
                self.current_word = word
                return True

            # Handle word definition end
            if word == ";":
                self._end_word_definition()
                return True

            # Handle control structures
            if word == "IF":
                return self._handle_if()
            elif word == "THEN":
                return self._handle_then()
            elif word == "ELSE":
                return self._handle_else()
            elif word == "BEGIN":
                if self.compiling:
                    self.word_definition.append(word)
                    return True
                return self._handle_begin()
            elif word == "UNTIL":
                if self.compiling:
                    self.word_definition.append(word)
                    return True
                return self._handle_until()
            elif word == "WHILE":
                if self.compiling:
                    self.word_definition.append(word)
                    return True
                return self._handle_while()
            elif word == "REPEAT":
                if self.compiling:
                    self.word_definition.append(word)
                    return True
                return self._handle_repeat()
            elif word == "RECURSE":
                return self._recurse()
            elif word == "DO":
                # If compiling, keep as token to be handled in compiled execution
                if self.compiling:
                    self.word_definition.append(word)
                    return True
                return self._handle_do()
            elif word == "LOOP":
                if self.compiling:
                    self.word_definition.append(word)
                    return True
                return self._handle_loop()

            # Handle variable operations
            if word == "VARIABLE":
                # Next token must be the variable name
                return self._handle_variable()
            elif word == "CONSTANT":
                return self._handle_constant()
            elif word == "!":
                return self._store()
            elif word == "@":
                return self._fetch()

            # Execute built-in or user-defined word
            # Handle ."string" inline printing tokens
            if word.startswith('."') and word.endswith('"'):
                # print inner content
                inner = word[2:-1]
                if self.compiling:
                    self.word_definition.append(word)
                else:
                    self.interpreter.log_output(inner)
                return True

            # Handle variable and constant names when they appear as words
            if word in self.variables:
                # pushing a variable reference (use name token)
                if self.compiling:
                    self.word_definition.append(word)
                else:
                    # push a simple reference (name) to the stack
                    self.data_stack.append({"type": "var", "name": word})
                return True

            if word in self.constants:
                if self.compiling:
                    self.word_definition.append(word)
                else:
                    self.data_stack.append(self.constants[word])
                return True

            if word in self.dictionary:
                if self.compiling:
                    self.word_definition.append(word)
                else:
                    result = self.dictionary[word]()
                    if result is False:  # Word execution failed
                        return False
                return True

            # Unknown word
            self.interpreter.log_output(f"Unknown word: {word}")
            return False

        except Exception as e:
            self.interpreter.debug_output(f"Word execution error: {e}")
            return False

    def _is_number(self, word):
        """Check if word is a number"""
        try:
            self._parse_number(word)
            return True
        except ValueError:
            return False

    def _parse_number(self, word):
        """Parse a number from string"""
        if "." in word:
            return float(word)
        else:
            return int(word)

    def _end_word_definition(self):
        """End word definition and store it"""
        if self.compiling and self.current_word:
            self.dictionary[self.current_word] = self._create_word_function(
                self.word_definition
            )
            self.interpreter.log_output(f"Defined word: {self.current_word}")
            self.compiling = False
            self.current_word = None
            self.word_definition = []
        else:
            self.interpreter.log_output("Error: Not in word definition")

    def _create_word_function(self, definition):
        """Create a function from word definition"""

        def word_func():
            i = 0
            # execute with instruction pointer so DO/LOOP can jump
            while i < len(definition):
                word = definition[i]

                # Handle DO/LOOP compiled control
                if word == "DO":
                    # DO expects ( limit start -- ) on stack
                    # Stack is: ... limit start
                    # start is on top
                    if len(self.data_stack) < 2:
                        self.interpreter.log_output("Stack underflow in DO")
                        return False
                    start = self.data_stack.pop()  # Top of stack is start index
                    limit = self.data_stack.pop()  # Next is limit
                    # push a frame with ip position and counters
                    frame = {
                        "type": "DO",
                        "ip": i,
                        "index": start,
                        "limit": limit,
                    }
                    self.return_stack.append(frame)
                    i += 1
                    continue

                if word == "LOOP":
                    if (
                        not self.return_stack
                        or self.return_stack[-1].get("type") != "DO"
                    ):
                        self.interpreter.log_output("LOOP without matching DO")
                        return False
                    frame = self.return_stack[-1]
                    frame["index"] += 1
                    # if still less than limit, jump back to after DO
                    if frame["index"] < frame["limit"]:
                        i = frame["ip"] + 1
                        continue
                    # else pop frame and continue
                    self.return_stack.pop()
                    i += 1
                    continue

                # Handle BEGIN...WHILE...REPEAT
                if word == "BEGIN":
                    # Mark the beginning of the loop
                    self.return_stack.append({"type": "BEGIN", "ip": i})
                    i += 1
                    continue

                if word == "WHILE":
                    # Check condition on stack
                    if len(self.data_stack) < 1:
                        self.interpreter.log_output("Stack underflow in WHILE")
                        return False
                    condition = self.data_stack.pop()
                    if condition == 0:  # False - skip to after REPEAT
                        # Find matching REPEAT
                        depth = 1
                        j = i + 1
                        while j < len(definition) and depth > 0:
                            if definition[j] == "BEGIN":
                                depth += 1
                            elif definition[j] == "REPEAT":
                                depth -= 1
                            j += 1
                        # Pop the BEGIN frame
                        if self.return_stack and self.return_stack[-1].get("type") == "BEGIN":
                            self.return_stack.pop()
                        i = j  # Jump past REPEAT
                        continue
                    i += 1
                    continue

                if word == "REPEAT":
                    # Jump back to BEGIN
                    if self.return_stack and self.return_stack[-1].get("type") == "BEGIN":
                        i = self.return_stack[-1]["ip"]
                        continue
                    i += 1
                    continue

                # Handle UNTIL
                if word == "UNTIL":
                    if len(self.data_stack) < 1:
                        self.interpreter.log_output("Stack underflow in UNTIL")
                        return False
                    condition = self.data_stack.pop()
                    if condition == 0:  # False - loop back to BEGIN
                        if self.return_stack and self.return_stack[-1].get("type") == "BEGIN":
                            i = self.return_stack[-1]["ip"]
                            continue
                    # True - exit loop
                    if self.return_stack and self.return_stack[-1].get("type") == "BEGIN":
                        self.return_stack.pop()
                    i += 1
                    continue

                # normal execution
                if not self._execute_word(word):
                    return False
                i += 1

            return True

        return word_func

    # Stack manipulation words
    def _dup(self):
        """Duplicate top of stack"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in DUP")
            return False
        self.data_stack.append(self.data_stack[-1])
        return True

    def _drop(self):
        """Drop top of stack"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in DROP")
            return False
        self.data_stack.pop()
        return True

    def _swap(self):
        """Swap top two stack items"""
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in SWAP")
            return False
        self.data_stack[-1], self.data_stack[-2] = (
            self.data_stack[-2],
            self.data_stack[-1],
        )
        return True

    def _over(self):
        """Copy second item to top"""
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in OVER")
            return False
        self.data_stack.append(self.data_stack[-2])
        return True

    def _rot(self):
        """Rotate top three items"""
        if len(self.data_stack) < 3:
            self.interpreter.log_output("Stack underflow in ROT")
            return False
        a, b, c = self.data_stack[-3], self.data_stack[-2], self.data_stack[-1]
        self.data_stack[-3], self.data_stack[-2], self.data_stack[-1] = b, c, a
        return True

    def _nip(self):
        """Remove second item"""
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in NIP")
            return False
        self.data_stack[-2] = self.data_stack[-1]
        self.data_stack.pop()
        return True

    def _tuck(self):
        """Copy top item under second item"""
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in TUCK")
            return False
        top = self.data_stack[-1]
        self.data_stack.insert(-1, top)
        return True

    # Arithmetic operations
    def _add(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in +")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(a + b)
        return True

    def _sub(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in -")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(a - b)
        return True

    def _mul(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in *")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(a * b)
        return True

    def _div(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in /")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        if b == 0:
            self.interpreter.log_output("Division by zero")
            return False
        self.data_stack.append(a / b)
        return True

    def _mod(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in MOD")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(a % b)
        return True

    def _negate(self):
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in NEGATE")
            return False
        self.data_stack[-1] = -self.data_stack[-1]
        return True

    def _abs(self):
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in ABS")
            return False
        self.data_stack[-1] = abs(self.data_stack[-1])
        return True

    def _one_plus(self):
        """Add 1 to top of stack"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in 1+")
            return False
        self.data_stack[-1] += 1
        return True

    def _one_minus(self):
        """Subtract 1 from top of stack"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in 1-")
            return False
        self.data_stack[-1] -= 1
        return True

    def _two_plus(self):
        """Add 2 to top of stack"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in 2+")
            return False
        self.data_stack[-1] += 2
        return True

    def _two_minus(self):
        """Subtract 2 from top of stack"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in 2-")
            return False
        self.data_stack[-1] -= 2
        return True

    def _two_times(self):
        """Multiply top of stack by 2"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in 2*")
            return False
        self.data_stack[-1] *= 2
        return True

    def _two_divide(self):
        """Divide top of stack by 2"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in 2/")
            return False
        self.data_stack[-1] //= 2
        return True

    def _min(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in MIN")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(min(a, b))
        return True

    def _max(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in MAX")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(max(a, b))
        return True

    # Comparison operations
    def _equal(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in =")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(-1 if a == b else 0)
        return True

    def _less(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in <")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(-1 if a < b else 0)
        return True

    def _greater(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in >")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(-1 if a > b else 0)
        return True

    def _less_equal(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in <=")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(-1 if a <= b else 0)
        return True

    def _greater_equal(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in >=")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(-1 if a >= b else 0)
        return True

    def _not_equal(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in <>")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(-1 if a != b else 0)
        return True

    # Logic operations
    def _and(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in AND")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(a & b)
        return True

    def _or(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in OR")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(a | b)
        return True

    def _xor(self):
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in XOR")
            return False
        b, a = self.data_stack.pop(), self.data_stack.pop()
        self.data_stack.append(a ^ b)
        return True

    def _invert(self):
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in INVERT")
            return False
        self.data_stack[-1] = ~self.data_stack[-1]
        return True

    # I/O operations
    def _dot(self):
        """Print top of stack"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in .")
            return False
        value = self.data_stack.pop()
        self.interpreter.log_output(str(value))
        return True

    def _dot_s(self):
        """Show stack contents"""
        if self.data_stack:
            stack_str = " ".join(str(x) for x in self.data_stack)
            self.interpreter.log_output(f"<{len(self.data_stack)}> {stack_str}")
        else:
            self.interpreter.log_output("<0>")
        return True

    def _cr(self):
        """Carriage return"""
        self.interpreter.log_output("")
        return True

    def _emit(self):
        """Emit character"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in EMIT")
            return False
        char_code = self.data_stack.pop()
        self.interpreter.log_output(chr(char_code))
        return True

    def _dot_quote(self):
        """Print string literal (.")"""
        # This is handled during tokenization - strings are already processed
        self.interpreter.log_output("." + " not implemented in this context")
        return True

    def _spaces(self):
        """Print n spaces"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in SPACES")
            return False
        n = self.data_stack.pop()
        self.interpreter.log_output(" " * n)
        return True

    # Math functions
    def _sin(self):
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in SIN")
            return False
        angle = math.radians(self.data_stack.pop())
        self.data_stack.append(math.sin(angle))
        return True

    def _cos(self):
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in COS")
            return False
        angle = math.radians(self.data_stack.pop())
        self.data_stack.append(math.cos(angle))
        return True

    def _tan(self):
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in TAN")
            return False
        angle = math.radians(self.data_stack.pop())
        self.data_stack.append(math.tan(angle))
        return True

    def _sqrt(self):
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in SQRT")
            return False
        value = self.data_stack.pop()
        if value < 0:
            self.interpreter.log_output("Cannot take square root of negative number")
            return False
        self.data_stack.append(math.sqrt(value))
        return True

    def _log(self):
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in LOG")
            return False
        value = self.data_stack.pop()
        if value <= 0:
            self.interpreter.log_output("Cannot take log of non-positive number")
            return False
        self.data_stack.append(math.log(value))
        return True

    def _exp(self):
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in EXP")
            return False
        self.data_stack.append(math.exp(self.data_stack.pop()))
        return True

    # Stack queries
    def _depth(self):
        """Push stack depth"""
        self.data_stack.append(len(self.data_stack))
        return True

    def _pick(self):
        """Pick nth item from stack"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in PICK")
            return False
        n = self.data_stack.pop()
        if n < 0 or n >= len(self.data_stack):
            self.interpreter.log_output("Invalid PICK index")
            return False
        self.data_stack.append(self.data_stack[-n - 1])
        return True

    def _roll(self):
        """Roll nth item to top"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in ROLL")
            return False
        n = self.data_stack.pop()
        if n < 0 or n >= len(self.data_stack):
            self.interpreter.log_output("Invalid ROLL index")
            return False
        item = self.data_stack[-n - 1]
        del self.data_stack[-n - 1]
        self.data_stack.append(item)
        return True

    # Control structures
    def _handle_if(self):
        """Handle IF"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in IF")
            return False

        condition = self.data_stack.pop()
        if condition == 0:  # False
            # Skip to ELSE or THEN
            self.return_stack.append("IF_SKIP")
        else:
            self.return_stack.append("IF_EXEC")
        return True

    def _handle_then(self):
        """Handle THEN"""
        if self.return_stack and self.return_stack[-1].startswith("IF"):
            self.return_stack.pop()
        return True

    def _handle_else(self):
        """Handle ELSE"""
        if self.return_stack and self.return_stack[-1] == "IF_EXEC":
            self.return_stack[-1] = "IF_SKIP"
        elif self.return_stack and self.return_stack[-1] == "IF_SKIP":
            self.return_stack[-1] = "IF_EXEC"
        return True

    def _handle_begin(self):
        """Handle BEGIN"""
        self.return_stack.append("BEGIN")
        return True

    def _handle_do(self):
        """Handle DO in interactive mode (push loop frame)"""
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in DO")
            return False
        start = self.data_stack.pop()  # Top of stack is start index
        limit = self.data_stack.pop()  # Next is limit
        self.return_stack.append(
            {"type": "DO", "ip": None, "index": start, "limit": limit}
        )
        return True

    def _handle_loop(self):
        """Handle LOOP in interactive mode"""
        if not self.return_stack or self.return_stack[-1].get("type") != "DO":
            self.interpreter.log_output("LOOP without matching DO")
            return False
        frame = self.return_stack[-1]
        frame["index"] += 1
        if frame["index"] >= frame["limit"]:
            self.return_stack.pop()
        return True

    def _handle_until(self):
        """Handle UNTIL"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in UNTIL")
            return False

        condition = self.data_stack.pop()
        if condition == 0:  # False, continue loop
            # Would need to jump back to BEGIN - simplified for now
            pass
        else:  # True, exit loop
            if self.return_stack and self.return_stack[-1] == "BEGIN":
                self.return_stack.pop()
        return True

    def _handle_while(self):
        """Handle WHILE"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in WHILE")
            return False

        condition = self.data_stack.pop()
        if condition == 0:  # False
            # Skip to REPEAT
            self.return_stack.append("WHILE_SKIP")
        else:
            self.return_stack.append("WHILE_EXEC")
        return True

    def _handle_repeat(self):
        """Handle REPEAT"""
        if self.return_stack and self.return_stack[-1].startswith("WHILE"):
            self.return_stack.pop()
        return True

    def _recurse(self):
        """Handle RECURSE - call the current word being defined"""
        if (
            self.compiling
            and self.current_word
            and self.current_word in self.dictionary
        ):
            # Call the current word recursively
            return self.dictionary[self.current_word]()
        else:
            self.interpreter.log_output(
                "RECURSE can only be used inside word definitions"
            )
            return False

    # Variables and constants
    def _handle_variable(self):
        """Handle VARIABLE declaration"""
        # Mark that the next token is the variable name to create.
        # Allow variable declaration both in interactive mode and inside definitions.
        self.expecting_variable_name = True
        return True

    def _handle_constant(self):
        """Handle CONSTANT declaration"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in CONSTANT")
            return False

        # Pop the value and wait for the next token to be the name
        value = self.data_stack.pop()
        self.pending_constant_value = value
        self.expecting_constant_name = True
        return True

    def _store(self):
        """Store value (!)"""
        # Expect: value address (address represented by {'type':'var','name':name}) OR name value
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in ! (store)")
            return False

        addr = self.data_stack.pop()
        value = self.data_stack.pop()

        # If addr is a variable ref dict
        if isinstance(addr, dict) and addr.get("type") == "var":
            varname = addr.get("name")
            self.variables[varname] = value
            return True

        # If addr is a string name
        if isinstance(addr, str) and addr in self.variables:
            self.variables[addr] = value
            return True

        # Unknown address
        self.interpreter.log_output("Invalid address for ! (store)")
        return False

    def _fetch(self):
        """Fetch value (@)"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in @ (fetch)")
            return False

        addr = self.data_stack.pop()
        if isinstance(addr, dict) and addr.get("type") == "var":
            varname = addr.get("name")
            self.data_stack.append(self.variables.get(varname, 0))
            return True

        if isinstance(addr, str) and addr in self.variables:
            self.data_stack.append(self.variables[addr])
            return True

        self.interpreter.log_output("Invalid address for @ (fetch)")
        return False

    # Gforth extension methods

    def _handle_locals_start(self):
        """Handle start of locals definition {"""
        if not self.compiling:
            self.interpreter.log_output(
                "Locals can only be defined in word definitions"
            )
            return False
        self.local_depth += 1
        return True

    def _handle_locals_end(self):
        """Handle end of locals definition }"""
        if not self.compiling:
            self.interpreter.log_output(
                "Locals can only be defined in word definitions"
            )
            return False
        self.local_depth -= 1
        return True

    # Floating point operations
    def _f_add(self):
        """Floating point addition"""
        if len(self.float_stack) < 2:
            self.interpreter.log_output("Float stack underflow in F+")
            return False
        b, a = self.float_stack.pop(), self.float_stack.pop()
        self.float_stack.append(a + b)
        return True

    def _f_sub(self):
        """Floating point subtraction"""
        if len(self.float_stack) < 2:
            self.interpreter.log_output("Float stack underflow in F-")
            return False
        b, a = self.float_stack.pop(), self.float_stack.pop()
        self.float_stack.append(a - b)
        return True

    def _f_mul(self):
        """Floating point multiplication"""
        if len(self.float_stack) < 2:
            self.interpreter.log_output("Float stack underflow in F*")
            return False
        b, a = self.float_stack.pop(), self.float_stack.pop()
        self.float_stack.append(a * b)
        return True

    def _f_div(self):
        """Floating point division"""
        if len(self.float_stack) < 2:
            self.interpreter.log_output("Float stack underflow in F/")
            return False
        b, a = self.float_stack.pop(), self.float_stack.pop()
        if b == 0:
            self.interpreter.log_output("Floating point division by zero")
            return False
        self.float_stack.append(a / b)
        return True

    def _f_dot(self):
        """Print floating point number"""
        if len(self.float_stack) < 1:
            self.interpreter.log_output("Float stack underflow in F.")
            return False
        value = self.float_stack.pop()
        self.interpreter.log_output(f"{value}")
        return True

    def _f_fetch(self):
        """Fetch floating point value from a variable/address onto float_stack"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in F@")
            return False

        addr = self.data_stack.pop()
        if isinstance(addr, dict) and addr.get("type") == "var":
            name = addr.get("name")
            value = self.variables.get(name, 0.0)
            try:
                self.float_stack.append(float(value))
                return True
            except (ValueError, TypeError):
                self.interpreter.log_output("Invalid float stored at variable")
                return False

        if isinstance(addr, str) and addr in self.variables:
            try:
                self.float_stack.append(float(self.variables[addr]))
                return True
            except (ValueError, TypeError):
                self.interpreter.log_output("Invalid float stored at variable")
                return False

        self.interpreter.log_output("Invalid address for F@")
        return False

    def _f_store(self):
        """Store floating value from float_stack or data_stack into variable/address"""
        # Prefer float stack, else use data_stack value
        if len(self.data_stack) < 1 and not self.float_stack:
            self.interpreter.log_output("Stack underflow in F! (store)")
            return False

        # Determine value
        if self.float_stack:
            value = self.float_stack.pop()
        else:
            value = self.data_stack.pop()

        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in F! (no address)")
            return False

        addr = self.data_stack.pop()
        if isinstance(addr, dict) and addr.get("type") == "var":
            self.variables[addr.get("name")] = float(value)
            return True
        if isinstance(addr, str) and addr in self.variables:
            self.variables[addr] = float(value)
            return True

        self.interpreter.log_output("Invalid address for F! (float store)")
        return False

    def _f_dup(self):
        """Duplicate top of float stack"""
        if len(self.float_stack) < 1:
            self.interpreter.log_output("Float stack underflow in FDUP")
            return False
        self.float_stack.append(self.float_stack[-1])
        return True

    def _f_drop(self):
        """Drop top of float stack"""
        if len(self.float_stack) < 1:
            self.interpreter.log_output("Float stack underflow in FDROP")
            return False
        self.float_stack.pop()
        return True

    def _f_swap(self):
        """Swap top two float stack items"""
        if len(self.float_stack) < 2:
            self.interpreter.log_output("Float stack underflow in FSWAP")
            return False
        self.float_stack[-1], self.float_stack[-2] = (
            self.float_stack[-2],
            self.float_stack[-1],
        )
        return True

    # Double precision operations
    def _d_add(self):
        """Double precision addition"""
        if len(self.data_stack) < 4:
            self.interpreter.log_output("Stack underflow in D+")
            return False
        d2_low, d2_high, d1_low, d1_high = (
            self.data_stack.pop(),
            self.data_stack.pop(),
            self.data_stack.pop(),
            self.data_stack.pop(),
        )
        result = (d1_high << 32 | d1_low) + (d2_high << 32 | d2_low)
        self.data_stack.append(result & 0xFFFFFFFF)  # low 32 bits
        self.data_stack.append(result >> 32)  # high 32 bits
        return True

    def _d_sub(self):
        """Double precision subtraction"""
        if len(self.data_stack) < 4:
            self.interpreter.log_output("Stack underflow in D-")
            return False
        d2_low, d2_high, d1_low, d1_high = (
            self.data_stack.pop(),
            self.data_stack.pop(),
            self.data_stack.pop(),
            self.data_stack.pop(),
        )
        result = (d1_high << 32 | d1_low) - (d2_high << 32 | d2_low)
        self.data_stack.append(result & 0xFFFFFFFF)  # low 32 bits
        self.data_stack.append(result >> 32)  # high 32 bits
        return True

    def _d_mul(self):
        """Double precision multiplication"""
        if len(self.data_stack) < 4:
            self.interpreter.log_output("Stack underflow in D*")
            return False
        d2_low, d2_high, d1_low, d1_high = (
            self.data_stack.pop(),
            self.data_stack.pop(),
            self.data_stack.pop(),
            self.data_stack.pop(),
        )
        result = (d1_high << 32 | d1_low) * (d2_high << 32 | d2_low)
        self.data_stack.append(result & 0xFFFFFFFF)  # low 32 bits
        self.data_stack.append(result >> 32)  # high 32 bits
        return True

    def _d_div(self):
        """Double precision division"""
        if len(self.data_stack) < 4:
            self.interpreter.log_output("Stack underflow in D/")
            return False
        d2_low, d2_high, d1_low, d1_high = (
            self.data_stack.pop(),
            self.data_stack.pop(),
            self.data_stack.pop(),
            self.data_stack.pop(),
        )
        divisor = d2_high << 32 | d2_low
        if divisor == 0:
            self.interpreter.log_output("Double precision division by zero")
            return False
        dividend = d1_high << 32 | d1_low
        result = dividend // divisor
        self.data_stack.append(result & 0xFFFFFFFF)  # low 32 bits
        self.data_stack.append(result >> 32)  # high 32 bits
        return True

    def _d_dot(self):
        """Print double precision number"""
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in D.")
            return False
        low, high = self.data_stack.pop(), self.data_stack.pop()
        value = (high << 32) | low
        self.interpreter.log_output(f"{value}")
        return True

    def _d_fetch(self):
        """Fetch double precision value from a variable/address.

        Pushes low, high components to stack.
        """
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in D@")
            return False

        addr = self.data_stack.pop()
        if isinstance(addr, dict) and addr.get("type") == "var":
            entry = self.variables.get(addr.get("name"))
            if isinstance(entry, (tuple, list)) and len(entry) == 2:
                low, high = entry
                self.data_stack.append(low)
                self.data_stack.append(high)
                return True
            self.interpreter.log_output("Invalid double value at variable")
            return False

        if isinstance(addr, str) and addr in self.variables:
            entry = self.variables[addr]
            if isinstance(entry, (tuple, list)) and len(entry) == 2:
                low, high = entry
                self.data_stack.append(low)
                self.data_stack.append(high)
                return True
            self.interpreter.log_output("Invalid double value at variable")
            return False

        self.interpreter.log_output("Invalid address for D@")
        return False

    def _d_store(self):
        """Store double precision value from stack into a variable/address as (low, high) tuple"""
        # Expect low high addr on stack or low, high, addr
        if len(self.data_stack) < 3:
            self.interpreter.log_output("Stack underflow in D! (store)")
            return False

        # Support two stack orders: (low high addr) or (addr high low)
        top = self.data_stack[-1]
        if isinstance(top, (dict, str)):
            # addr is on top
            addr = self.data_stack.pop()
            # then high then low
            if len(self.data_stack) < 2:
                self.interpreter.log_output("Stack underflow in D! (store)")
                return False
            high = self.data_stack.pop()
            low = self.data_stack.pop()
        else:
            # assume low high addr ordering
            low = self.data_stack.pop()
            high = self.data_stack.pop()
            addr = self.data_stack.pop()

        if isinstance(addr, dict) and addr.get("type") == "var":
            self.variables[addr.get("name")] = (low, high)
            return True
        if isinstance(addr, str):
            self.variables[addr] = (low, high)
            return True

        self.interpreter.log_output("Invalid address for D! (double store)")
        return False

    def _i(self):
        """Push current loop index (I)"""
        if not self.return_stack:
            self.interpreter.log_output("I used outside of DO/LOOP")
            return False
        frame = self.return_stack[-1]
        if frame.get("type") != "DO":
            self.interpreter.log_output("I used outside of DO/LOOP")
            return False
        self.data_stack.append(frame.get("index", 0))
        return True

    # Memory allocation
    def _allocate(self):
        """Allocate memory block"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in ALLOCATE")
            return False
        size = self.data_stack.pop()
        try:
            block_id = self.next_memory_id
            self.memory_blocks[block_id] = bytearray(size)
            self.next_memory_id += 1
            self.data_stack.append(block_id)  # address
            self.data_stack.append(0)  # success flag
        except (MemoryError, ValueError):
            self.data_stack.append(0)  # null address
            self.data_stack.append(-1)  # error flag
        return True

    def _free(self):
        """Free allocated memory"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in FREE")
            return False
        addr = self.data_stack.pop()
        if addr in self.memory_blocks:
            del self.memory_blocks[addr]
            self.data_stack.append(0)  # success
        else:
            self.data_stack.append(-1)  # error
        return True

    def _resize(self):
        """Resize allocated memory"""
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in RESIZE")
            return False
        new_size, addr = self.data_stack.pop(), self.data_stack.pop()
        if addr in self.memory_blocks:
            try:
                self.memory_blocks[addr] = self.memory_blocks[addr][
                    :new_size
                ] + bytearray(max(0, new_size - len(self.memory_blocks[addr])))
                self.data_stack.append(addr)  # new address
                self.data_stack.append(0)  # success
            except (MemoryError, ValueError):
                self.data_stack.append(0)  # null
                self.data_stack.append(-1)  # error
        else:
            self.data_stack.append(0)  # null
            self.data_stack.append(-1)  # error
        return True

    # File operations
    def _open_file(self):
        """Open a file"""
        if len(self.data_stack) < 2:
            self.interpreter.log_output("Stack underflow in OPEN-FILE")
            return False
        fam, addr = self.data_stack.pop(), self.data_stack.pop()
        # For educational purposes, simulate file operations
        self.interpreter.log_output(
            f"OPEN-FILE simulated for address {addr} (educational mode)"
        )
        file_id = self.next_file_id
        self.files[file_id] = {
            "name": f"file_{file_id}",
            "mode": fam,
            "address": addr,
        }
        self.next_file_id += 1
        self.data_stack.append(file_id)  # fileid
        self.data_stack.append(0)  # ior
        return True

    def _close_file(self):
        """Close a file"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in CLOSE-FILE")
            return False
        fileid = self.data_stack.pop()
        if fileid in self.files:
            del self.files[fileid]
            self.data_stack.append(0)  # ior
        else:
            self.data_stack.append(-1)  # error
        return True

    def _read_file(self):
        """Read from file"""
        self.interpreter.log_output("READ-FILE simulated (educational mode)")
        return True

    def _write_file(self):
        """Write to file"""
        self.interpreter.log_output("WRITE-FILE simulated (educational mode)")
        return True

    def _file_position(self):
        """Get file position"""
        self.interpreter.log_output("FILE-POSITION simulated (educational mode)")
        return True

    def _reposition_file(self):
        """Set file position"""
        self.interpreter.log_output("REPOSITION-FILE simulated (educational mode)")
        return True

    # String operations
    def _compare(self):
        """Compare two strings"""
        if len(self.data_stack) < 4:
            self.interpreter.log_output("Stack underflow in COMPARE")
            return False
        len2, addr2, len1, addr1 = (
            self.data_stack.pop(),
            self.data_stack.pop(),
            self.data_stack.pop(),
            self.data_stack.pop(),
        )
        # Simplified string comparison
        str1 = f"string_at_{addr1}"[:len1]
        str2 = f"string_at_{addr2}"[:len2]
        result = (str1 > str2) - (str1 < str2)  # -1, 0, or 1
        self.data_stack.append(result)
        return True

    def _search(self):
        """Search for substring"""
        if len(self.data_stack) < 4:
            self.interpreter.log_output("Stack underflow in SEARCH")
            return False
        len2, addr2, len1, addr1 = (
            self.data_stack.pop(),
            self.data_stack.pop(),
            self.data_stack.pop(),
            self.data_stack.pop(),
        )
        # Simplified substring search
        haystack = f"string_at_{addr1}"[:len1]
        needle = f"string_at_{addr2}"[:len2]
        pos = haystack.find(needle)
        if pos >= 0:
            self.data_stack.append(len1 - pos)  # remaining length
            self.data_stack.append(addr1 + pos)  # found address
            self.data_stack.append(-1)  # found flag
        else:
            self.data_stack.append(len1)  # original length
            self.data_stack.append(addr1)  # original address
            self.data_stack.append(0)  # not found flag
        return True

    def _sliteral(self):
        """Compile string literal"""
        self.interpreter.log_output("SLITERAL simulated")
        return True

    # Exception handling
    def _try(self):
        """Start exception handling"""
        self.exception_handlers.append(len(self.return_stack))
        return True

    def _throw(self):
        """Throw exception"""
        if len(self.data_stack) < 1:
            self.interpreter.log_output("Stack underflow in THROW")
            return False
        error_code = self.data_stack.pop()
        if error_code != 0:
            self.interpreter.log_output(f"Exception thrown: {error_code}")
            # Unwind stack to exception handler
            if self.exception_handlers:
                handler_depth = self.exception_handlers.pop()
                while len(self.return_stack) > handler_depth:
                    self.return_stack.pop()
        return True

    def _catch(self):
        """End exception handling"""
        if self.exception_handlers:
            self.exception_handlers.pop()
        return True

    # Value (mutable constants)
    def _value(self):
        """Create a mutable constant"""
        if not self.compiling:
            self.interpreter.log_output("VALUE can only be used in definitions")
            return False
        # Next word will be the value name
        return True

    def _to(self):
        """Assign to a VALUE"""
        self.interpreter.log_output("TO (value assignment) simulated")
        return True

    # Structure operations
    def _struct(self):
        """Start structure definition"""
        self.interpreter.log_output("STRUCT definition started")
        return True

    def _field(self):
        """Define structure field"""
        self.interpreter.log_output("FIELD defined")
        return True

    def _end_struct(self):
        """End structure definition"""
        self.interpreter.log_output("STRUCT definition ended")
        return True

    # Object operations
    def _object(self):
        """Start object definition"""
        self.interpreter.log_output("OBJECT definition started")
        return True

    def _method(self):
        """Define object method"""
        self.interpreter.log_output("METHOD defined")
        return True

    def _end_object(self):
        """End object definition"""
        self.interpreter.log_output("OBJECT definition ended")
        return True

    def _new(self):
        """Create new object instance"""
        self.interpreter.log_output("NEW object created")
        return True

    def _send(self):
        """Send message to object"""
        self.interpreter.log_output("SEND message to object")
        return True
