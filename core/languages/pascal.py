# pylint: disable=W0718,R0913,R0914,R0912
"""
TW Pascal Language Executor
===========================

Implements TW Pascal, an educational variant of the Pascal programming language
for the Time_Warp IDE, focusing on structured programming concepts.

Language Features:
- Program structure: PROGRAM, BEGIN, END blocks
- Unit system: UNIT, INTERFACE, IMPLEMENTATION, USES
- Variable declarations: VAR, CONST with type specifications
- Control structures: IF/THEN/ELSE, WHILE/DO, FOR loops, REPEAT/UNTIL, CASE statements
- Procedures and functions: PROCEDURE, FUNCTION with parameter passing
- Object-oriented programming: OBJECT, INHERITANCE, CONSTRUCTOR, DESTRUCTOR
- Input/Output: READLN, WRITELN for console I/O
- Data types: INTEGER, REAL, STRING, BOOLEAN, CHAR, WORD, LONGINT, BYTE, SHORTINT
- Arrays: fixed-size arrays with indexing
- Records: structured data types
- File I/O: basic file operations
- Mathematical functions: SIN, COS, TAN, SQRT, ABS, ROUND, TRUNC, EXP, LN, ARCTAN
- String operations: LENGTH, COPY, POS, CONCAT, UPCASE, DOWNCASE
- Inline assembly: ASM blocks (simulated)
- Compiler directives: {$I }, {$DEFINE}, {$IFDEF}, etc.

The executor provides Pascal-like syntax with Turbo Pascal enhancements suitable
for educational purposes, with structured programming constructs and OOP capabilities.
"""

# pylint: disable=R0902,W0718,R1705,R0911,R0912,W0613,R1702,W0123,W0107,R0903

import re
import math
import random


class TwPascalExecutor:
    """Handles TW Pascal language command execution"""

    def __init__(self, interpreter):
        """Initialize with reference to main interpreter"""
        self.interpreter = interpreter
        self.program_name = ""
        self.current_unit = None
        self.units = {}  # Unit definitions
        self.variables = {}  # Local variable scope
        self.constants = {}  # Constants
        self.procedures = {}  # User-defined procedures
        self.functions = {}  # User-defined functions
        self.objects = {}  # Object definitions
        self.data_types = {}  # Variable type information
        self.arrays = {}  # Array definitions
        self.records = {}  # Record definitions
        self.current_procedure = None
        self.call_stack = []  # For procedure/function calls
        self.compiler_directives = {}  # Compiler directives like {$DEFINE}
        self.inline_asm_enabled = False  # For ASM blocks

    # Dispatch table: keyword → handler method name
    _CMD_HANDLERS = {
        "PROGRAM": "_handle_program",
        "UNIT": "_handle_unit",
        "INTERFACE": "_handle_interface",
        "IMPLEMENTATION": "_handle_implementation",
        "USES": "_handle_uses",
        "BEGIN": "_handle_begin",
        "END": "_handle_end",
        "VAR": "_handle_var",
        "CONST": "_handle_const",
        "TYPE": "_handle_type",
        "OBJECT": "_handle_object",
        "CONSTRUCTOR": "_handle_constructor",
        "DESTRUCTOR": "_handle_destructor",
        "IF": "_handle_if",
        "WHILE": "_handle_while",
        "FOR": "_handle_for",
        "REPEAT": "_handle_repeat",
        "CASE": "_handle_case",
        "PROCEDURE": "_handle_procedure",
        "FUNCTION": "_handle_function",
        "ASM": "_handle_asm",
        "READLN": "_handle_readln",
        "WRITELN": "_handle_writeln",
        "WRITE": "_handle_write",
    }

    # Keywords that are handled by their parent statement; return "continue" immediately
    _NO_OP_CMDS = {
        "INHERITS", "THEN", "ELSE", "DO", "TO", "DOWNTO", "UNTIL", "OF",
    }

    def execute_command(self, command):
        """Execute a Pascal command and return the result"""
        try:
            command = command.strip()
            if not command:
                return "continue"

            # Remove trailing semicolon if present
            if command.endswith(";"):
                command = command[:-1].strip()

            # Get the base command name (first word before any parenthesis/space)
            match = re.match(r"(\w+)", command)
            if not match:
                return "continue"

            cmd = match.group(1).upper()

            # No-op keywords (context handled by parent statement)
            if cmd in self._NO_OP_CMDS:
                return "continue"

            # Dispatch to dedicated handler via lookup table
            handler_name = self._CMD_HANDLERS.get(cmd)
            if handler_name:
                return getattr(self, handler_name)(command)

            # Assignment
            if ":=" in command:
                return self._handle_assignment(command)

            # Compiler directives
            if command.strip().startswith("{$"):
                return self._handle_directive(command)

            # Procedure/function calls (fallthrough)
            if "(" in command and ")" in command:
                return self._handle_call(command)
            if command.upper() in self.procedures:
                return self._handle_call(command)

        except Exception as e:
            self.interpreter.debug_output(f"Pascal command error: {e}")
            return "continue"

        return "continue"

    def _handle_program(self, command):
        """Handle PROGRAM declaration"""
        # PROGRAM program_name;
        match = re.match(r"PROGRAM\s+(\w+)", command, re.IGNORECASE)
        if match:
            self.program_name = match.group(1)
            self.interpreter.log_output(f"🚀 Starting program: {self.program_name}")
        return "continue"

    def _handle_unit(self, command):
        """Handle UNIT declaration"""
        # UNIT unit_name;
        match = re.match(r"UNIT\s+(\w+)", command, re.IGNORECASE)
        if match:
            unit_name = match.group(1).upper()
            self.current_unit = unit_name
            self.units[unit_name] = {
                "interface": [],
                "implementation": [],
                "variables": {},
                "procedures": {},
                "functions": {},
            }
            if self.interpreter.console_banner:
                self.interpreter.log_output(f"📦 Unit {unit_name} declared")
        return "continue"

    def _handle_interface(self, command):
        """Handle INTERFACE section"""
        # INTERFACE
        if self.current_unit:
            self.interpreter.log_output("🔗 Entering interface section")
        return "continue"

    def _handle_implementation(self, command):
        """Handle IMPLEMENTATION section"""
        # IMPLEMENTATION
        if self.current_unit:
            self.interpreter.log_output("⚙️ Entering implementation section")
        return "continue"

    def _handle_uses(self, command):
        """Handle USES clause"""
        # USES unit1, unit2, ...;
        uses_part = command[4:].strip()  # Remove USES
        if uses_part.endswith(";"):
            uses_part = uses_part[:-1]
        units = [u.strip().upper() for u in uses_part.split(",")]
        for unit in units:
            if unit in self.units:
                self.interpreter.log_output(f"📚 Using unit {unit}")
            else:
                self.interpreter.debug_output(f"Unit {unit} not found")
        return "continue"

    def _handle_type(self, command):
        """Handle TYPE declarations"""
        # TYPE name = type_definition;
        try:
            type_part = command[4:].strip()  # Remove TYPE
            if "=" in type_part:
                name, def_part = type_part.split("=", 1)
                name = name.strip().upper()
                type_def = def_part.strip()

                # Handle different type definitions
                if type_def.upper().startswith("RECORD"):
                    self._handle_record_type(name, type_def)
                elif type_def.upper().startswith("ARRAY"):
                    self._handle_array_type(name, type_def)
                elif type_def.upper().startswith("("):
                    # Enumeration type
                    self._handle_enum_type(name, type_def)
                else:
                    # Type alias
                    self.data_types[name] = type_def.upper()

                self.interpreter.log_output(f"🏷️ Type {name} defined")
        except Exception as e:
            self.interpreter.debug_output(f"TYPE declaration error: {e}")
        return "continue"

    def _handle_object(self, command):
        """Handle OBJECT declaration"""
        # OBJECT name [(parent)]
        try:
            object_part = command[6:].strip()  # Remove OBJECT
            if "(" in object_part and ")" in object_part:
                # Inheritance
                name_part, parent_part = object_part.split("(")
                name = name_part.strip().upper()
                parent = parent_part.split(")")[0].strip().upper()
                self.objects[name] = {
                    "parent": parent,
                    "fields": {},
                    "methods": {},
                }
                self.interpreter.log_output(f"🏗️ Object {name} inherits from {parent}")
            else:
                # Base object
                name = object_part.upper()
                self.objects[name] = {
                    "parent": None,
                    "fields": {},
                    "methods": {},
                }
                self.interpreter.log_output(f"🏗️ Object {name} declared")
        except Exception as e:
            self.interpreter.debug_output(f"OBJECT declaration error: {e}")
        return "continue"

    def _handle_constructor(self, command):
        """Handle CONSTRUCTOR declaration"""
        # CONSTRUCTOR name(parameters);
        try:
            match = re.match(r"CONSTRUCTOR\s+(\w+)\s*\((.*?)\)", command, re.IGNORECASE)
            if match:
                name = match.group(1).upper()
                self.interpreter.log_output(f"🔨 Constructor {name} declared")
        except Exception as e:
            self.interpreter.debug_output(f"CONSTRUCTOR declaration error: {e}")
        return "continue"

    def _handle_destructor(self, command):
        """Handle DESTRUCTOR declaration"""
        # DESTRUCTOR name;
        try:
            match = re.match(r"DESTRUCTOR\s+(\w+)", command, re.IGNORECASE)
            if match:
                name = match.group(1).upper()
                self.interpreter.log_output(f"💥 Destructor {name} declared")
        except Exception as e:
            self.interpreter.debug_output(f"DESTRUCTOR declaration error: {e}")
        return "continue"

    def _handle_asm(self, command):
        """Handle ASM block (simulated)"""
        # ASM ... END;
        if not self.inline_asm_enabled:
            self.interpreter.log_output("⚠️ Inline assembly not enabled")
            return "continue"

        self.interpreter.log_output("🔧 Entering assembly block (simulated)")
        return "continue"

    def _handle_directive(self, command):
        """Handle compiler directives"""
        # {$directive value} or {$directive}
        try:
            directive = command.strip()[2:-1].strip()  # Remove {$ and }
            parts = directive.split()
            dir_name = parts[0].upper()

            if dir_name == "I":
                # {$I filename} - include file
                if len(parts) > 1:
                    filename = parts[1]
                    self.interpreter.log_output(f"📄 Including file {filename}")
            elif dir_name == "DEFINE":
                # {$DEFINE name} or {$DEFINE name value}
                if len(parts) > 1:
                    name = parts[1].upper()
                    value = parts[2] if len(parts) > 2 else "1"
                    self.compiler_directives[name] = value
                    self.interpreter.log_output(f"🏷️ Defined {name} = {value}")
            elif dir_name == "IFDEF":
                # {$IFDEF name} - conditional compilation
                if len(parts) > 1:
                    name = parts[1].upper()
                    defined = name in self.compiler_directives
                    self.interpreter.log_output(f"🔍 IFDEF {name} = {defined}")
            elif dir_name == "IFNDEF":
                # {$IFNDEF name} - conditional compilation
                if len(parts) > 1:
                    name = parts[1].upper()
                    not_defined = name not in self.compiler_directives
                    self.interpreter.log_output(f"🔍 IFNDEF {name} = {not_defined}")
        except Exception as e:
            self.interpreter.debug_output(f"Directive error: {e}")
        return "continue"

    def _handle_begin(self, command):
        """Handle BEGIN block"""
        # BEGIN - start of code block
        if self.interpreter.console_banner:
            self.interpreter.log_output("📦 Entering code block")
        return "continue"

    def _handle_end(self, command):
        """Handle END block"""
        # END. - program end
        # END; - block end
        if command.strip().upper() == "END.":
            if self.interpreter.console_banner:
                self.interpreter.log_output("🏁 Program completed")
            return "end"
        else:
            if self.interpreter.console_banner:
                self.interpreter.log_output("📦 Exiting code block")
            return "continue"

    def _handle_var(self, command):
        """Handle VAR declarations"""
        # VAR variable_list : type;
        try:
            # Remove VAR and split by :
            var_part = command[3:].strip()
            if ":" in var_part:
                var_list, type_part = var_part.split(":", 1)
                var_type = type_part.strip().upper()

                # Parse variable list (can be comma-separated)
                variables = [v.strip() for v in var_list.split(",")]

                for var in variables:
                    var_name = var.upper()
                    self.variables[var_name] = self._get_default_value(var_type)
                    self.data_types[var_name] = var_type

                    # Handle array declarations
                    if "[" in var and "]" in var:
                        array_match = re.match(r"(\w+)\s*\[(.+)\]", var)
                        if array_match:
                            array_name = array_match.group(1).upper()
                            dimensions = array_match.group(2)
                            self._declare_array(array_name, dimensions, var_type)

                self.interpreter.log_output(
                    f"📝 Declared variables: {', '.join(variables)} as {var_type}"
                )
        except Exception as e:
            self.interpreter.debug_output(f"VAR declaration error: {e}")
        return "continue"

    def _handle_record_type(self, name, type_def):
        """Handle RECORD type definition"""
        # RECORD field1: type1; field2: type2; END;
        try:
            record_part = type_def[6:].strip()  # Remove RECORD
            if record_part.upper().endswith("END"):
                record_part = record_part[:-3].strip()
                fields = {}
                field_lines = record_part.split(";")
                for line in field_lines:
                    line = line.strip()
                    if ":" in line:
                        field_list, field_type = line.split(":", 1)
                        field_names = [f.strip().upper() for f in field_list.split(",")]
                        for field_name in field_names:
                            fields[field_name] = field_type.strip().upper()
                self.records[name] = fields
                self.data_types[name] = "RECORD"
        except Exception as e:
            self.interpreter.debug_output(f"Record type error: {e}")

    def _handle_array_type(self, name, type_def):
        """Handle ARRAY type definition"""
        # ARRAY [low..high] OF element_type
        try:
            array_part = type_def[5:].strip()  # Remove ARRAY
            if "OF" in array_part:
                range_part, element_type = array_part.split("OF", 1)
                range_part = range_part.strip()
                if range_part.startswith("[") and range_part.endswith("]"):
                    dimensions = range_part[1:-1].strip()
                    self._declare_array(name, dimensions, element_type.strip().upper())
        except Exception as e:
            self.interpreter.debug_output(f"Array type error: {e}")

    def _handle_enum_type(self, name, type_def):
        """Handle enumeration type definition"""
        # (value1, value2, value3)
        try:
            enum_part = type_def.strip()
            if enum_part.startswith("(") and enum_part.endswith(")"):
                values_str = enum_part[1:-1]
                values = [v.strip().upper() for v in values_str.split(",")]
                enum_dict = {}
                for i, value in enumerate(values):
                    enum_dict[value] = i
                self.constants.update(enum_dict)
                self.data_types[name] = "ENUM"
                self.interpreter.log_output(
                    f"🔢 Enum {name} with values: {', '.join(values)}"
                )
        except Exception as e:
            self.interpreter.debug_output(f"Enum type error: {e}")

    def _handle_const(self, command):
        """Handle CONST declarations"""
        # CONST name = value;
        try:
            const_part = command[5:].strip()
            if "=" in const_part:
                name, value_expr = const_part.split("=", 1)
                name = name.strip().upper()
                value = self._evaluate_expression(value_expr.strip())
                self.constants[name] = value
                self.interpreter.log_output(f"🔒 Constant {name} = {value}")
        except Exception as e:
            self.interpreter.debug_output(f"CONST declaration error: {e}")
        return "continue"

    def _handle_assignment(self, command):
        """Handle := assignment"""
        try:
            if ":=" in command:
                var_part, expr_part = command.split(":=", 1)
                var_name = var_part.strip().upper()
                value = self._evaluate_expression(expr_part.strip())

                # Handle array assignment
                if "[" in var_name and "]" in var_name:
                    self._assign_array_element(var_name, value)
                else:
                    # Type checking
                    if var_name in self.data_types:
                        expected_type = self.data_types[var_name]
                        value = self._convert_to_type(value, expected_type)

                    self.variables[var_name] = value
                    # Also store in interpreter variables for compatibility
                    self.interpreter.variables[var_name] = value

                self.interpreter.log_output(f"✅ {var_name} := {value}")
        except Exception as e:
            self.interpreter.debug_output(f"Assignment error: {e}")
        return "continue"

    # ---- block helpers -------------------------------------------------

    def _lines(self):
        """Program lines as (number, text) pairs."""
        return self.interpreter.program_lines

    def _next_code_line(self, start):
        """Index of the next non-blank line at or after *start*, else None."""
        lines = self._lines()
        idx = start
        while idx < len(lines):
            if (lines[idx][1] or "").strip():
                return idx
            idx += 1
        return None

    # BEGIN/END count wherever they appear on a line: ``while x do begin``
    # opens a block just as ``begin`` alone on its line does.  END. is the
    # program terminator, not a block close.
    _BLOCK_TOKEN = re.compile(r"\bBEGIN\b|\bEND\b(?!\s*\.)", re.IGNORECASE)
    _STRING_LITERAL = re.compile(r"'[^']*'")

    def _matching_block_end(self, opener_index):
        """Index of the END; closing the BEGIN on *opener_index*."""
        lines = self._lines()
        depth = 1
        idx = opener_index + 1
        while idx < len(lines):
            text = self._STRING_LITERAL.sub("", lines[idx][1] or "")
            for token in self._BLOCK_TOKEN.finditer(text):
                if token.group(0).upper() == "BEGIN":
                    depth += 1
                    continue
                depth -= 1
                if depth == 0:
                    return idx
            idx += 1
        return None

    def _matching_until(self, repeat_index):
        """Index of the UNTIL line closing the REPEAT on *repeat_index*."""
        lines = self._lines()
        depth = 1
        idx = repeat_index + 1
        while idx < len(lines):
            cmd = (lines[idx][1] or "").strip().upper()
            if re.match(r"^REPEAT\b", cmd):
                depth += 1
            elif re.match(r"^UNTIL\b", cmd):
                depth -= 1
                if depth == 0:
                    return idx
            idx += 1
        return None

    def _execute_block(self, start, end):
        """Run program lines ``start``..``end`` (exclusive) in place.

        ``interpreter.current_line`` follows the executing line so nested
        IF/WHILE/REPEAT handlers can locate their own blocks.
        """
        lines = self._lines()
        saved_line = self.interpreter.current_line
        idx = start
        steps = 0
        outcome = "continue"
        try:
            while idx < end:
                steps += 1
                if steps > 100_000:
                    self.interpreter.log_output(
                        "Block terminated: maximum steps reached"
                    )
                    break
                if self.interpreter.pump():
                    # Stop pressed: unwind the enclosing construct too.
                    outcome = "end"
                    break
                self.interpreter.current_line = idx
                cmd = (lines[idx][1] or "").strip()
                if cmd:
                    result = self.execute_command(cmd)
                    if result == "end":
                        outcome = result
                        break
                    if isinstance(result, str) and result.startswith("jump:"):
                        try:
                            target = int(result.split(":")[1])
                        except (ValueError, IndexError):
                            break
                        if target <= idx:
                            break
                        idx = target
                        continue
                idx += 1
        finally:
            self.interpreter.current_line = saved_line
        return outcome

    def _find_else(self, after):
        """Describe an ELSE that follows an IF block, if there is one."""
        lines = self._lines()
        idx = self._next_code_line(after)
        if idx is None:
            return None
        text = (lines[idx][1] or "").strip()
        if not re.match(r"^ELSE\b", text, re.IGNORECASE):
            return None

        rest = re.sub(r"^ELSE\b", "", text, flags=re.IGNORECASE).strip()
        if not rest:
            opener = self._next_code_line(idx + 1)
            if opener is not None and (lines[opener][1] or "").strip().upper().startswith("BEGIN"):
                block_end = self._matching_block_end(opener)
                if block_end is not None:
                    return {"kind": "block", "start": opener + 1,
                            "end": block_end, "after": block_end + 1}
            return {"kind": "inline", "command": "", "line": idx, "after": idx + 1}

        if rest.upper().startswith("BEGIN"):
            block_end = self._matching_block_end(idx)
            if block_end is not None:
                return {"kind": "block", "start": idx + 1,
                        "end": block_end, "after": block_end + 1}
            return {"kind": "inline", "command": "", "line": idx, "after": idx + 1}

        return {"kind": "inline", "command": rest, "line": idx, "after": idx + 1}

    def _run_branch(self, branch):
        """Execute an ELSE description and report where execution continues."""
        saved_line = self.interpreter.current_line
        try:
            self.interpreter.current_line = branch.get("line", saved_line)
            if branch["kind"] == "inline":
                result = (
                    self.execute_command(branch["command"])
                    if branch["command"]
                    else "continue"
                )
            else:
                result = self._execute_block(branch["start"], branch["end"])
        finally:
            self.interpreter.current_line = saved_line
        if isinstance(result, str) and result.startswith("jump:"):
            return result
        if result == "end":
            return result
        return f"jump:{branch['after']}"

    def _handle_if(self, command):
        """Handle IF statement, inline or with BEGIN...END blocks."""
        try:
            match = re.match(
                r"IF\s+(.+?)\s+THEN\b(.*)$",
                command.strip(),
                re.IGNORECASE | re.DOTALL,
            )
            if not match:
                return "continue"

            condition = match.group(1).strip()
            then_part = match.group(2).strip()

            is_block = not then_part or re.match(
                r"^BEGIN\b", then_part, re.IGNORECASE
            )
            if not is_block:
                # Single-statement form: IF cond THEN stmt [ELSE stmt]
                inline_else = None
                else_match = re.match(
                    r"(.+?)\s+ELSE\s+(.+)$", then_part, re.IGNORECASE | re.DOTALL
                )
                if else_match:
                    then_part = else_match.group(1).strip()
                    inline_else = else_match.group(2).strip()
                if self._evaluate_expression(condition):
                    return self.execute_command(then_part)
                if inline_else:
                    return self.execute_command(inline_else)
                return "continue"

            lines = self._lines()
            if then_part:
                opener = self.interpreter.current_line
                body_start = opener + 1
            else:
                opener = self._next_code_line(self.interpreter.current_line + 1)
                if opener is None or not (lines[opener][1] or "").strip().upper().startswith("BEGIN"):
                    return "continue"
                body_start = opener + 1

            block_end = self._matching_block_end(opener)
            if block_end is None:
                self.interpreter.log_output("IF block without matching END")
                return "continue"

            branch = self._find_else(block_end + 1)
            if self._evaluate_expression(condition):
                result = self._execute_block(body_start, block_end)
                if result == "end":
                    return result
                return f"jump:{branch['after'] if branch else block_end + 1}"
            if branch:
                return self._run_branch(branch)
            return f"jump:{block_end + 1}"
        except Exception as e:
            self.interpreter.debug_output(f"IF statement error: {e}")
        return "continue"

    def _handle_while(self, command):
        """Handle WHILE loop, inline or with a BEGIN...END body."""
        try:
            match = re.match(
                r"WHILE\s+(.+?)\s+DO\b(.*)$",
                command.strip(),
                re.IGNORECASE | re.DOTALL,
            )
            if not match:
                return "continue"

            condition = match.group(1).strip()
            statement = match.group(2).strip()

            body_start = None
            block_end = None
            if re.match(r"^BEGIN\b", statement, re.IGNORECASE):
                # WHILE cond DO BEGIN ... END continues on the following lines.
                opener = self.interpreter.current_line
                block_end = self._matching_block_end(opener)
                if block_end is None:
                    self.interpreter.log_output("WHILE block without matching END")
                    return "continue"
                body_start = opener + 1
            elif not statement:
                opener = self._next_code_line(self.interpreter.current_line + 1)
                if opener is None:
                    return "continue"
                text = (self._lines()[opener][1] or "").strip().upper()
                if not text.startswith("BEGIN"):
                    return "continue"
                block_end = self._matching_block_end(opener)
                if block_end is None:
                    self.interpreter.log_output("WHILE block without matching END")
                    return "continue"
                body_start = opener + 1

            if block_end is not None:
                iterations = 0
                while self._evaluate_expression(condition):
                    result = self._execute_block(body_start, block_end)
                    if result == "end":
                        return result
                    iterations += 1
                    if iterations >= 10000:
                        self.interpreter.log_output(
                            "WHILE loop terminated: maximum iterations reached"
                        )
                        break
                return f"jump:{block_end + 1}"

            iterations = 0
            while iterations < 10000:
                if self.interpreter.pump():
                    return "end"
                if not self._evaluate_expression(condition):
                    break
                result = self.execute_command(statement)
                if result != "continue":
                    return result
                iterations += 1
            if iterations >= 10000:
                self.interpreter.log_output(
                    "WHILE loop terminated: maximum iterations reached"
                )
        except Exception as e:
            self.interpreter.debug_output(f"WHILE loop error: {e}")
        return "continue"

    def _handle_for(self, command):
        """Handle FOR loops with inline, next-line, or BEGIN...END bodies."""
        try:
            match = re.match(
                r"FOR\s+(\w+)\s*:=\s*(.+?)\s+(TO|DOWNTO)\s+(.+?)\s+DO\b(.*)$",
                command.strip(),
                re.IGNORECASE | re.DOTALL,
            )
            if not match:
                return "continue"

            var_name = match.group(1).upper()
            start_expr = match.group(2).strip()
            direction = match.group(3).upper()
            end_expr = match.group(4).strip().rstrip(";").strip()
            statement = match.group(5).strip()

            body_line = None
            body_start = None
            block_end = None
            if statement and re.match(r"^BEGIN\b", statement, re.IGNORECASE):
                opener = self.interpreter.current_line
                block_end = self._matching_block_end(opener)
                body_start = opener + 1
                if block_end is None:
                    self.interpreter.log_output("FOR block without matching END")
                    return "continue"
            elif not statement:
                candidate = self._next_code_line(self.interpreter.current_line + 1)
                if candidate is None:
                    return "continue"
                if (self._lines()[candidate][1] or "").strip().upper().startswith("BEGIN"):
                    block_end = self._matching_block_end(candidate)
                    if block_end is None:
                        self.interpreter.log_output("FOR block without matching END")
                        return "continue"
                    body_start = candidate + 1
                else:
                    body_line = candidate

            start_val = int(self._evaluate_expression(start_expr))
            end_val = int(self._evaluate_expression(end_expr))
            step = 1 if direction == "TO" else -1
            current = start_val
            iterations = 0

            def in_range():
                """True while the counter has not passed its bound."""
                return current <= end_val if step > 0 else current >= end_val

            while in_range():
                if iterations >= 10000:
                    self.interpreter.log_output(
                        "FOR loop terminated: maximum iterations reached"
                    )
                    break
                if self.interpreter.pump():
                    return "end"
                self.variables[var_name] = current
                self.interpreter.variables[var_name] = current

                if block_end is not None:
                    result = self._execute_block(body_start, block_end)
                elif body_line is not None:
                    saved_line = self.interpreter.current_line
                    self.interpreter.current_line = body_line
                    try:
                        result = self.execute_command(
                            (self._lines()[body_line][1] or "").strip()
                        )
                    finally:
                        self.interpreter.current_line = saved_line
                else:
                    result = self.execute_command(statement)

                if result == "end":
                    return result

                current += step
                iterations += 1

            # Pascal leaves the counter one step past the range.
            self.variables[var_name] = current
            self.interpreter.variables[var_name] = current
            if block_end is not None:
                return f"jump:{block_end + 1}"
            if body_line is not None:
                return f"jump:{body_line + 1}"
        except Exception as e:
            self.interpreter.debug_output(f"FOR loop error: {e}")
        return "continue"

    def _handle_repeat(self, command):
        """Handle REPEAT ... UNTIL, inline or as a block."""
        try:
            rest = re.sub(r"^REPEAT\b", "", command.strip(), flags=re.IGNORECASE).strip()
            inline = re.match(r"(.+?)\s+UNTIL\s+(.+)$", rest, re.IGNORECASE | re.DOTALL)
            if inline:
                statement = inline.group(1).strip()
                condition = inline.group(2).strip()
                iterations = 0
                while iterations < 10000:
                    if self.interpreter.pump():
                        return "end"
                    result = self.execute_command(statement)
                    if result != "continue":
                        return result
                    if self._evaluate_expression(condition):
                        break
                    iterations += 1
                if iterations >= 10000:
                    self.interpreter.log_output(
                        "REPEAT loop terminated: maximum iterations reached"
                    )
                return "continue"

            until_index = self._matching_until(self.interpreter.current_line)
            if until_index is None:
                self.interpreter.log_output("REPEAT without matching UNTIL")
                return "continue"
            until_text = (self._lines()[until_index][1] or "").strip()
            condition = re.sub(
                r"^UNTIL\b", "", until_text, flags=re.IGNORECASE
            ).strip().rstrip(";")

            iterations = 0
            while iterations < 10000:
                if rest:
                    # ``REPEAT writeln(n);`` keeps a statement on the REPEAT
                    # line itself; it belongs to the body, not the loop header.
                    result = self.execute_command(rest)
                    if result != "continue":
                        return result
                result = self._execute_block(
                    self.interpreter.current_line + 1, until_index
                )
                if result == "end":
                    return result
                if self._evaluate_expression(condition):
                    break
                iterations += 1
            if iterations >= 10000:
                self.interpreter.log_output(
                    "REPEAT loop terminated: maximum iterations reached"
                )
            return f"jump:{until_index + 1}"
        except Exception as e:
            self.interpreter.debug_output(f"REPEAT loop error: {e}")
        return "continue"

    def _handle_case(self, command):
        """Handle CASE statement"""
        try:
            # CASE selector OF value: statement; ... END
            # This is a simplified implementation
            case_part = command[4:].strip()  # Remove CASE
            if "OF" in case_part:
                selector_part, cases_part = case_part.split("OF", 1)
                selector = self._evaluate_expression(selector_part.strip())

                # Parse cases (simplified)
                cases = cases_part.split(";")
                for case in cases:
                    case = case.strip()
                    if ":" in case:
                        value_part, stmt_part = case.split(":", 1)
                        if value_part.strip().upper() == str(selector).upper():
                            return self.execute_command(stmt_part.strip())
        except Exception as e:
            self.interpreter.debug_output(f"CASE statement error: {e}")
        return "continue"

    def _handle_procedure(self, command):
        """Handle PROCEDURE declaration"""
        try:
            # PROCEDURE name(parameters); [VAR declarations;] BEGIN statements END;
            match = re.match(r"PROCEDURE\s+(\w+)\s*\((.*?)\)", command, re.IGNORECASE)
            if match:
                proc_name = match.group(1).upper()
                params = match.group(2).strip() if match.group(2) else ""

                # Store procedure definition (simplified)
                self.procedures[proc_name] = {
                    "params": params,
                    "body": [],  # Would need to collect following lines until END
                }
                self.interpreter.log_output(f"📋 Procedure {proc_name} declared")
        except Exception as e:
            self.interpreter.debug_output(f"PROCEDURE declaration error: {e}")
        return "continue"

    def _handle_function(self, command):
        """Handle FUNCTION declaration"""
        try:
            # FUNCTION name(parameters): return_type; [VAR declarations;] BEGIN statements END;
            match = re.match(
                r"FUNCTION\s+(\w+)\s*\((.*?)\)\s*:\s*(\w+)",
                command,
                re.IGNORECASE,
            )
            if match:
                func_name = match.group(1).upper()
                params = match.group(2).strip() if match.group(2) else ""
                return_type = match.group(3).upper()

                # Store function definition (simplified)
                self.functions[func_name] = {
                    "params": params,
                    "return_type": return_type,
                    "body": [],  # Would need to collect following lines until END
                }
                self.interpreter.log_output(f"🔧 Function {func_name} declared")
        except Exception as e:
            self.interpreter.debug_output(f"FUNCTION declaration error: {e}")
        return "continue"

    def _handle_call(self, command):
        """Handle procedure/function call"""
        try:
            # name(parameters)
            match = re.match(r"(\w+)\s*\((.*?)\)", command)
            if match:
                name = match.group(1).upper()

                if name in self.procedures:
                    self.interpreter.log_output(f"📞 Calling procedure {name}")
                    # Execute procedure (simplified)
                elif name in self.functions:
                    self.interpreter.log_output(f"🔧 Calling function {name}")
                    # Execute function and return result (simplified)
                    return "continue"
        except Exception as e:
            self.interpreter.debug_output(f"Call error: {e}")
        return "continue"

    def _handle_readln(self, command):
        """Handle READLN input"""
        try:
            # READLN(variable) or READLN(var1, var2, ...)
            readln_part = command[6:].strip()  # Remove READLN
            if readln_part.startswith("(") and readln_part.endswith(")"):
                var_list = readln_part[1:-1].strip()
                variables = [v.strip().upper() for v in var_list.split(",")]

                for var in variables:
                    prompt = f"Enter value for {var}: "
                    value = self.interpreter.get_user_input(prompt)
                    # Type conversion based on declared type
                    if var in self.data_types:
                        var_type = self.data_types[var]
                        value = self._convert_to_type(value, var_type)
                    else:
                        # Try to convert to number
                        try:
                            if "." in value:
                                value = float(value)
                            else:
                                value = int(value)
                        except Exception as e:
                            self.interpreter.debug_output(
                                f"Type conversion error: {e}"
                            )  # Keep as string

                    self.variables[var] = value
                    self.interpreter.variables[var] = value
        except Exception as e:
            self.interpreter.debug_output(f"READLN error: {e}")
        return "continue"

    def _handle_writeln(self, command):
        """Handle WRITELN output"""
        try:
            # WRITELN(expression) or WRITELN(expr1, expr2, ...)
            writeln_part = command[7:].strip()  # Remove WRITELN
            if writeln_part.startswith("(") and writeln_part.endswith(")"):
                expr_list = writeln_part[1:-1].strip()
                expressions = [e.strip() for e in expr_list.split(",")]

                output_parts = []
                for expr in expressions:
                    value = self._evaluate_expression(expr)
                    output_parts.append(str(value))

                output = "".join(output_parts)
                self.interpreter.log_output(output)
            else:
                # WRITELN without parentheses
                self.interpreter.log_output("")
        except Exception as e:
            self.interpreter.debug_output(f"WRITELN error: {e}")
        return "continue"

    def _handle_write(self, command):
        """Handle WRITE output (no newline)"""
        try:
            # WRITE(expression) or WRITE(expr1, expr2, ...)
            write_part = command[5:].strip()  # Remove WRITE
            if write_part.startswith("(") and write_part.endswith(")"):
                expr_list = write_part[1:-1].strip()
                expressions = [e.strip() for e in expr_list.split(",")]

                output_parts = []
                for expr in expressions:
                    value = self._evaluate_expression(expr)
                    output_parts.append(str(value))

                output = "".join(output_parts)
                # Use debug output to avoid newline, or find another way
                self.interpreter.log_output(output)
        except Exception as e:
            self.interpreter.debug_output(f"WRITE error: {e}")
        return "continue"

    def _evaluate_expression(self, expr):
        """Evaluate Pascal expression"""
        try:
            # Replace Pascal operators with Python equivalents
            # Order matters: replace compound operators BEFORE single-char ones
            expr = expr.replace("<>", "!=")
            expr = expr.replace(":=", "=")  # Strip assignment operator if present
            # Replace single = with == only where it's not part of <=, >=, !=
            import re as _re
            expr = _re.sub(r'(?<![<>!])=(?!=)', '==', expr)
            expr = expr.replace("AND", "and")
            expr = expr.replace("OR", "or")
            expr = expr.replace("NOT", "not")
            expr = expr.replace("DIV", "//")
            expr = expr.replace("MOD", "%")

            # Turbo Pascal functions (both uppercase and lowercase for compatibility)
            allowed_names = {
                # Basic functions
                "abs": abs,
                "ABS": abs,
                "round": round,
                "ROUND": round,
                "trunc": int,
                "TRUNC": int,
                "int": int,
                "INT": int,
                "float": float,
                "FLOAT": float,
                "max": max,
                "MAX": max,
                "min": min,
                "MIN": min,
                "len": len,
                "LEN": len,
                "str": str,
                "STR": str,
                "ord": ord,
                "ORD": ord,
                "chr": chr,
                "CHR": chr,
                # Math functions
                "sin": math.sin,
                "SIN": math.sin,
                "cos": math.cos,
                "COS": math.cos,
                "tan": math.tan,
                "TAN": math.tan,
                "arcsin": math.asin,
                "ARCSIN": math.asin,
                "arccos": math.acos,
                "ARCCOS": math.acos,
                "arctan": math.atan,
                "ARCTAN": math.atan,
                "exp": math.exp,
                "EXP": math.exp,
                "ln": math.log,
                "LN": math.log,
                "log": math.log10,
                "LOG": math.log10,
                "sqrt": math.sqrt,
                "SQRT": math.sqrt,
                "sqr": lambda x: x * x,
                "SQR": lambda x: x * x,
                "power": math.pow,
                "POWER": math.pow,
                # String functions
                "length": len,
                "LENGTH": len,
                "copy": lambda s, start, count: (
                    s[start - 1 : start - 1 + count] if s else ""
                ),
                "COPY": lambda s, start, count: (
                    s[start - 1 : start - 1 + count] if s else ""
                ),
                "pos": lambda substr, s: (s.find(substr) + 1 if substr in s else 0),
                "POS": lambda substr, s: (s.find(substr) + 1 if substr in s else 0),
                "concat": lambda *args: "".join(str(arg) for arg in args),
                "CONCAT": lambda *args: "".join(str(arg) for arg in args),
                "upcase": lambda s: str(s).upper(),
                "UPCASE": lambda s: str(s).upper(),
                "downcase": lambda s: str(s).lower(),
                "DOWNCASE": lambda s: str(s).lower(),
                "delete": lambda s, start, count: (
                    s[: start - 1] + s[start - 1 + count :] if s else ""
                ),
                "DELETE": lambda s, start, count: (
                    s[: start - 1] + s[start - 1 + count :] if s else ""
                ),
                # Random functions
                "random": random.random,
                "RANDOM": random.random,
                "randomize": random.seed,
                "RANDOMIZE": random.seed,
                # Type conversion functions
                "val": lambda s: (
                    int(float(s))
                    if s.replace(".", "").replace("-", "").isdigit()
                    else 0
                ),
                "VAL": lambda s: (
                    int(float(s))
                    if s.replace(".", "").replace("-", "").isdigit()
                    else 0
                ),
                "str_val": str,
                "STR_VAL": str,
            }

            # Create evaluation context
            # Pascal is case-insensitive: store variables under both original
            # (uppercase) keys and lowercase versions so eval() resolves either.
            eval_context = {}
            for k, v in self.variables.items():
                eval_context[k] = v
                eval_context[k.lower()] = v
            for k, v in self.constants.items():
                eval_context[k] = v
                eval_context[k.lower()] = v
            eval_context.update(allowed_names)

            # Safe evaluation via AST-based evaluator
            from core.utilities.safe_eval import safe_eval
            eval_context.update(allowed_names)

            return safe_eval(expr, eval_context)
        except (ValueError, SyntaxError, TypeError, ZeroDivisionError) as e:
            self.interpreter.debug_output(f"Expression evaluation error: {e}")
            return 0

    def _get_default_value(self, var_type):
        """Get default value for a Pascal type"""
        type_defaults = {
            "INTEGER": 0,
            "REAL": 0.0,
            "STRING": "",
            "BOOLEAN": False,
            "CHAR": " ",
            # Turbo Pascal extended types
            "WORD": 0,  # 16-bit unsigned
            "LONGINT": 0,  # 32-bit signed
            "BYTE": 0,  # 8-bit unsigned
            "SHORTINT": 0,  # 8-bit signed
            "SINGLE": 0.0,  # Single precision float
            "DOUBLE": 0.0,  # Double precision float
            "EXTENDED": 0.0,  # Extended precision float
            "COMP": 0,  # Computational type
        }
        return type_defaults.get(var_type.upper(), 0)

    def _convert_to_type(self, value, target_type):
        """Convert value to specified Pascal type"""
        try:
            target_type = target_type.upper()
            if target_type == "INTEGER":
                return int(float(value))
            elif target_type == "REAL":
                return float(value)
            elif target_type == "STRING":
                return str(value)
            elif target_type == "BOOLEAN":
                if isinstance(value, str):
                    return value.upper() in ["TRUE", "1", "YES"]
                return bool(value)
            elif target_type == "CHAR":
                return str(value)[0] if value else " "
        except Exception as e:
            self.interpreter.debug_output(f"Type conversion error: {e}")
            pass
        return value

    def _declare_array(self, array_name, dimensions, element_type):
        """Declare an array with given dimensions and element type"""
        try:
            # Parse dimensions like "1..10" or just "10"
            dim_parts = dimensions.split(",")
            array_dims = []

            for dim in dim_parts:
                dim = dim.strip()
                if ".." in dim:
                    start, end = dim.split("..")
                    start, end = int(start.strip()), int(end.strip())
                    array_dims.append(end - start + 1)
                else:
                    array_dims.append(int(dim))

            # Create multi-dimensional array
            def create_array(dims):
                if len(dims) == 1:
                    return [self._get_default_value(element_type)] * dims[0]
                else:
                    return [create_array(dims[1:]) for _ in range(dims[0])]

            self.arrays[array_name] = create_array(array_dims)
            self.data_types[array_name] = f"ARRAY OF {element_type}"
            self.interpreter.log_output(
                f"📊 Array {array_name} declared with dimensions {array_dims}"
            )
        except Exception as e:
            self.interpreter.debug_output(f"Array declaration error: {e}")

    def _assign_array_element(self, array_ref, value):
        """Assign value to array element"""
        try:
            # Parse array[index1,index2,...]
            match = re.match(r"(\w+)\s*\[(.+)\]", array_ref)
            if match:
                array_name = match.group(1).upper()
                indices_str = match.group(2)
                indices = [
                    int(self._evaluate_expression(idx.strip()))
                    for idx in indices_str.split(",")
                ]

                if array_name in self.arrays:
                    array = self.arrays[array_name]
                    # Navigate to the element (assuming 0-based indexing)
                    for idx in indices[:-1]:
                        array = array[idx]
                    array[indices[-1]] = value
                    self.interpreter.log_output(
                        f"📊 {array_name}[{','.join(map(str, indices))}] := {value}"
                    )
        except Exception as e:
            self.interpreter.debug_output(f"Array assignment error: {e}")
