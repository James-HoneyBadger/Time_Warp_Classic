# pylint: disable=W0718,R0913,R0911,R0912,R0915,C0301
"""
TW PILOT Language Executor
==========================

Implements the TW PILOT (Time_Warp Programmed Inquiry, Learning, Or Teaching) programming
language for the Time_Warp IDE. TW PILOT is an educational language designed for simple,
structured programming with built-in support for user interaction and turtle graphics.

Language Features:
- Text output with variable interpolation (T:)
- User input collection (A:)
- Conditional branching (Y:, N:)
- Program flow control (J:, L:)
- Variable management (U:)
- Pattern matching (M:, MT:)
- Mathematical operations (MATH:)
- Game development commands (GAME:)
- Audio control (AUDIO:)
- File operations (F:)
- Web requests (W:)
- Database operations (D:)
- String manipulation (S:)
- Date/time functions (DT:)
- Branching logic (BRANCH:)
- Multimedia support (MULTIMEDIA:)
- Data storage (STORAGE:)
- Subroutine calls (C:)
- Runtime system commands (R:)

The executor parses PILOT commands (identified by the colon syntax) and executes
them using the main interpreter's facilities for output, input, variables, and graphics.
"""

# pylint: disable=C0301,R1705,W0718,W0212,R0912,R0915,C0415,W0613

import re
import random

# pylint: disable=C0302,R0903,R0914,R1702


class TwPilotExecutor:
    """
    Executor for TW PILOT programming language commands.

    Handles parsing and execution of PILOT statements, which use a colon-prefixed
    syntax (e.g., T:, A:, J:). Each command type has a specific handler method
    that implements the required functionality.

    The executor works closely with the main Time_WarpInterpreter to access
    shared resources like variables, output functions, and turtle graphics.
    """

    def __init__(self, interpreter):
        """
        Initialize the PILOT executor.

        Args:
            interpreter: Reference to the main Time_WarpInterpreter instance
        """
        self.interpreter = interpreter

        # PILOT 73 Features
        self.arrays = {}  # Array storage: name -> list
        self.return_stack = []  # For U: (Use) subroutines
        self.system_vars = {
            "answer": "",  # %answer - last input
            "matched": "",  # %matched - matched text from M:
            "left": "",  # %left - text left of match
            "right": "",  # %right - text right of match
            "status": 0,  # %status - operation status
            "maxuses": 10,  # %maxuses - max subroutine nesting
        }
        self.screen_control = {
            "cursor_row": 0,
            "cursor_col": 0,
            "screen_cleared": False,
        }

    def execute_command(
        self, command
    ):  # pylint: disable=too-many-return-statements,too-many-branches
        """
        Execute a PILOT command and return the execution result.

        Parses the command to determine its type based on the colon prefix,
        then routes execution to the appropriate handler method.

        Args:
            command (str): The PILOT command to execute

        Returns:
            str: Execution result ("continue", "end", or jump target)
        """
        try:
            # Robust command type detection for J: and J(...):
            if command.startswith("J:") or command.startswith("J("):
                cmd_type = "J:"
            else:
                colon_idx = command.find(":")
                if colon_idx != -1:
                    cmd_type = command[: colon_idx + 1]
                else:
                    cmd_type = command[:2] if len(command) > 1 else command

            # Route to appropriate handler based on command type
            if cmd_type == "T:":
                return self._handle_text_output(command)
            elif cmd_type == "A:":
                return self._handle_accept_input(command)
            elif cmd_type == "Y:":
                return self._handle_yes_condition(command)
            elif cmd_type == "N:":
                return self._handle_no_condition(command)
            elif cmd_type == "J:":
                return self._handle_jump(command)
            elif cmd_type == "M:":
                return self._handle_match_jump(command)
            elif cmd_type == "MT:":
                return self._handle_match_text(command)
            elif cmd_type == "C:":
                return self._handle_compute_or_return(command)
            elif cmd_type == "R:":
                return self._handle_runtime_command(command)
            elif cmd_type == "GAME:":
                return self._handle_game_command(command)
            elif cmd_type == "AUDIO:":
                return self._handle_audio_command(command)
            elif cmd_type == "F:":
                return self._handle_file_command(command)
            elif cmd_type == "W:":
                return self._handle_web_command(command)
            elif cmd_type == "D:":
                # D: is overloaded for
                # both database operations (D:OPEN/QUERY/INSERT)
                # and array dimensioning syntax
                # (e.g. ARR(3)). Prefer array handling
                # if the payload looks like a
                # dimension spec (has parentheses at end).
                payload = command[2:].strip()
                if payload and "(" in payload and payload.endswith(")"):
                    return self._handle_dimension_array(command)
                return self._handle_database_command(command)
            elif cmd_type == "S:":
                return self._handle_string_command(command)
            elif cmd_type == "DT:":
                return self._handle_datetime_command(command)
            elif cmd_type == "MATH:":
                return self._handle_math_command(command)
            elif cmd_type == "BRANCH:":
                return self._handle_branch_command(command)
            elif cmd_type == "MULTIMEDIA:":
                return self._handle_multimedia_command(command)
            elif cmd_type == "STORAGE:":
                return self._handle_storage_command(command)
            elif cmd_type == "G:":
                return self._handle_graphics_command(command)
            elif cmd_type == "L:":
                # Label definition - no execution needed
                return "continue"
            elif cmd_type == "U:":
                return self._handle_use_subroutine(command)
            # Dimension arrays handled above as part of D:.
            elif cmd_type == "PA:":
                return self._handle_pause(command)
            elif cmd_type == "CH:":
                return self._handle_clear_home(command)
            elif cmd_type == "CA:":
                return self._handle_cursor_address(command)
            elif cmd_type == "CL:":
                return self._handle_clear_line(command)
            elif cmd_type == "CE:":
                return self._handle_clear_end(command)
            elif cmd_type == "JM:":
                return self._handle_jump_match(command)
            elif cmd_type == "TH:":
                return self._handle_type_hang(command)
            elif cmd_type == "XS:":
                return self._handle_system_command(command)
            elif cmd_type == "PR:":
                return self._handle_problem(command)
            elif cmd_type == "E:":
                return self._handle_end_subroutine(command)
            elif command.strip().upper() == "END":
                return "end"

        except Exception as e:  # pylint: disable=broad-except
            self.interpreter.debug_output(f"PILOT command error: {e}")
            return "continue"

        return "continue"

    def _handle_text_output(self, command):
        """Handle T: text output command"""
        text = command[2:].strip()
        # If the previous command set a match (Y: or N:), then this T: is
        # treated as conditional and only prints when match_flag is True.
        if self.interpreter._last_match_set:  # pylint: disable=protected-access
            # consume the sentinel
            self.interpreter._last_match_set = False  # pylint: disable=protected-access
            if not self.interpreter.match_flag:
                # do not print when match is false
                return "continue"

        text = self.interpreter.interpolate_text(text)
        self.interpreter.log_output(text)
        return "continue"

    def _handle_accept_input(self, command):
        """Handle A: accept input command (PILOT 73 compatible)"""
        var_spec = command[2:].strip()

        # PILOT 73: If no variable specified, use %answer system variable
        if not var_spec:
            var_name = "%answer"
            prompt = "Input: "
        else:
            var_name = var_spec
            prompt = f"Enter value for {var_name}: "

        # Log the input prompt to user output
        self.interpreter.log_output(f"Awaiting input: {prompt}")

        value = self.interpreter.get_user_input(prompt)

        # Store in system variables if it's a % variable
        if var_name.startswith("%"):
            self.system_vars[var_name[1:]] = value if value is not None else ""
        else:
            # Distinguish numeric and alphanumeric input for regular variables
            if value is not None and value.strip() != "":
                try:
                    # Accept int if possible, else float, else string
                    if value.isdigit() or (
                        value.startswith("-") and value[1:].isdigit()
                    ):
                        self.interpreter.variables[var_name] = int(value)
                    else:
                        float_val = float(value)
                        self.interpreter.variables[var_name] = float_val
                except (ValueError, TypeError):
                    self.interpreter.variables[var_name] = value
            else:
                self.interpreter.variables[var_name] = ""

        # Debug: show type and value of input variable
        if var_name.startswith("%"):
            self.interpreter.debug_output(
                f"[DEBUG] %{var_name[1:]} = {self.system_vars[var_name[1:]]!r}"
            )
        else:
            self.interpreter.debug_output(
                f"[DEBUG] {var_name} = {self.interpreter.variables[var_name]!r} "
                f"(type: {type(self.interpreter.variables[var_name]).__name__})"
            )
        return "continue"

    def _handle_yes_condition(self, command):
        """Handle Y: match if condition is true"""
        condition = command[2:].strip()
        try:
            result = self.interpreter.evaluate_expression(condition)
            self.interpreter.match_flag = bool(result)
        except Exception:
            self.interpreter.match_flag = False
        # mark that the last command set the match
        # flag so a following T: can be conditional
        self.interpreter._last_match_set = True
        return "continue"

    def _handle_no_condition(self, command):
        """Handle N: match if condition is false"""
        condition = command[2:].strip()
        try:
            result = self.interpreter.evaluate_expression(condition)
            # N: treat like a plain conditional
            # (match when the condition is TRUE).
            self.interpreter.match_flag = bool(result)
        except Exception:
            # On error, default to no match
            self.interpreter.match_flag = False
        # mark that the last command set the match
        # flag so a following T: can be conditional
        self.interpreter._last_match_set = True
        return "continue"

    def _handle_jump(self, command):
        """Handle J: jump command (conditional or unconditional)"""
        # Robustly detect conditional jump: J(<condition>):<label> using regex

        match = re.match(r"^J\((.+)\):(.+)$", command.strip())
        if match:
            condition = match.group(1).strip()
            label = match.group(2).strip()
            try:
                cond_val = self.interpreter.evaluate_expression(condition)
                self.interpreter.debug_output(
                    f"[DEBUG] Condition string: '{condition}', AGE = "
                    f"{self.interpreter.variables.get('AGE', None)} "
                    f"(type: {type(self.interpreter.variables.get('AGE', None)).__name__})"
                )
                is_true = False
                if isinstance(cond_val, bool):
                    is_true = cond_val
                elif isinstance(cond_val, (int, float)):
                    is_true = cond_val != 0
                elif isinstance(cond_val, str):
                    is_true = cond_val.strip().lower() in ("true", "1")
                self.interpreter.debug_output(
                    f"[DEBUG] Evaluating condition: {condition} => {cond_val!r} "
                    f"(type: {type(cond_val).__name__}), interpreted as {is_true}"
                )
                if is_true:
                    self.interpreter.debug_output(
                        f"[DEBUG] Attempting to jump to label '{label}'. Labels dict: {self.interpreter.labels}"
                    )
                    if label in self.interpreter.labels:
                        self.interpreter.debug_output(
                            f"🎯 Condition '{condition}' is TRUE, jumping to {label} (line {self.interpreter.labels[label]})"
                        )
                        return f"jump:{self.interpreter.labels[label]}"
                    else:
                        self.interpreter.debug_output(
                            f"⚠️ Label '{label}' not found. Labels dict: {self.interpreter.labels}"
                        )
                else:
                    self.interpreter.debug_output(
                        f"🚫 Condition '{condition}' is FALSE, continuing"
                    )
                return "continue"
            except Exception as e:
                self.interpreter.debug_output(
                    f"❌ Error evaluating condition '{condition}': {e}"
                )
                return "continue"

        # If not conditional, treat as unconditional jump
        rest = command[2:].strip()
        label = rest
        if self.interpreter._last_match_set:
            self.interpreter._last_match_set = False
            if not self.interpreter.match_flag:
                return "continue"
        self.interpreter.debug_output(
            f"[DEBUG] Unconditional jump to label '{label}'. Labels dict: {self.interpreter.labels}"
        )
        if label in self.interpreter.labels:
            self.interpreter.debug_output(
                f"[DEBUG] Unconditional jump to {label} (line {self.interpreter.labels[label]})"
            )
            return f"jump:{self.interpreter.labels[label]}"
        else:
            self.interpreter.debug_output(
                f"⚠️ Unconditional jump label '{label}' not found. Labels dict: {self.interpreter.labels}"
            )
        return "continue"

    def _handle_match_jump(self, command):
        """Handle M: pattern matching command (PILOT 73 compatible)"""
        pattern = command[2:].strip()

        # Get text to match against (%answer system variable)
        text_to_match = self.system_vars.get("answer", "")

        # PILOT 73 pattern matching with wildcards
        # ? matches any single character
        # * matches any sequence of characters
        # | separates alternatives
        # , separates additional alternatives

        # Split pattern on | and , to get alternatives
        alternatives = []
        for alt in pattern.replace(",", "|").split("|"):
            alternatives.append(alt.strip())

        # Try each alternative
        for alt_pattern in alternatives:
            if self._matches_pilot_pattern(text_to_match, alt_pattern):
                # Found a match
                self.system_vars["matched"] = text_to_match
                self.system_vars["left"] = ""
                self.system_vars["right"] = ""
                self.interpreter.match_flag = True

                # Set match-related system variables
                match_pos = text_to_match.find(
                    alt_pattern.replace("?", ".").replace("*", ".*")
                )
                if match_pos >= 0:
                    self.system_vars["left"] = text_to_match[:match_pos]
                    self.system_vars["right"] = text_to_match[
                        match_pos + len(alt_pattern) :
                    ]

                self.interpreter.debug_output(
                    f"[DEBUG] Pattern '{alt_pattern}' matched in '{text_to_match}'"
                )
                return "continue"

        # No match found
        self.system_vars["matched"] = ""
        self.system_vars["left"] = ""
        self.system_vars["right"] = ""
        self.interpreter.match_flag = False

        self.interpreter.debug_output(
            f"[DEBUG] No pattern match found for '{pattern}' in '{text_to_match}'"
        )
        return "continue"

    def _matches_pilot_pattern(self, text, pattern):
        """Check if text matches PILOT 73 pattern with wildcards"""
        # Convert PILOT wildcards to regex
        # ? -> .
        # * -> .*
        regex_pattern = pattern.replace("?", ".").replace("*", ".*")
        try:
            return bool(re.search(regex_pattern, text, re.IGNORECASE))
        except Exception:
            # If regex fails, fall back to simple string matching
            return pattern.lower() in text.lower()

    def _handle_match_text(self, command):
        """Handle MT: match-conditional text output"""
        text = command[3:].strip()
        if self.interpreter.match_flag:
            text = self.interpreter.interpolate_text(text)
            self.interpreter.log_output(text)
        return "continue"

    def _handle_compute_or_return(self, command):
        """Handle C: compute or return command"""
        payload = command[2:].strip()
        if payload == "":
            if self.interpreter.stack:
                return f"jump:{self.interpreter.stack.pop()}"
            return "continue"
        if "=" in payload:
            var_part, expr_part = payload.split("=", 1)
            var_name = var_part.strip().rstrip(":")
            expr = expr_part.strip()
            try:
                value = self.interpreter.evaluate_expression(expr)
                self.interpreter.variables[var_name] = value
            except Exception as e:
                self.interpreter.debug_output(f"Error in compute C: {payload}: {e}")
            return "continue"
        # Unrecognized payload after C:, ignore
        return "continue"

    def _handle_use_subroutine(self, command):
        """Handle U: use subroutine command (PILOT 73)"""
        label = command[2:].strip()

        # Check nesting limit
        if len(self.return_stack) >= self.system_vars.get("maxuses", 10):
            self.interpreter.debug_output(
                f"Error: Maximum subroutine nesting level ({self.system_vars['maxuses']}) exceeded"
            )
            return "continue"

        # Find current line number (simplified - we'll use a placeholder)
        current_line = 0  # This would need to be passed from the interpreter

        # Push return address to stack
        self.return_stack.append(current_line)

        # Jump to subroutine
        if label in self.interpreter.labels:
            self.interpreter.debug_output(f"[DEBUG] Calling subroutine {label}")
            return f"jump:{self.interpreter.labels[label]}"
        else:
            self.interpreter.debug_output(
                f"Error: Subroutine label '{label}' not found"
            )
            # Pop the return address since we can't call the subroutine
            self.return_stack.pop()
            return "continue"

    def _handle_end_subroutine(self, command):
        """Handle E: end subroutine command (PILOT 73)"""
        # Return from subroutine if we have a return address
        if self.return_stack:
            return_line = self.return_stack.pop()
            self.interpreter.debug_output(
                f"[DEBUG] Returning from subroutine to line {return_line}"
            )
            return f"jump:{return_line}"
        else:
            # No subroutine to return from, end program
            self.interpreter.debug_output(
                "[DEBUG] No active subroutine, ending program"
            )
            return "end"

    def _handle_runtime_command(self, command):
        """Handle R: runtime commands - placeholder for now"""
        # This would contain the full
        # implementation from the original interpreter
        self.interpreter.log_output(f"Runtime command: {command[2:].strip()}")
        return "continue"

    def _handle_game_command(self, command):
        """Handle GAME: game development commands - placeholder for now"""
        # This would contain the full
        # implementation from the original interpreter
        self.interpreter.log_output(f"Game command: {command[5:].strip()}")
        return "continue"

    def _handle_audio_command(self, command):
        """Handle AUDIO: audio system commands - placeholder for now"""
        # This would contain the full
        # implementation from the original interpreter
        self.interpreter.log_output(f"Audio command: {command[6:].strip()}")
        return "continue"

    def _handle_file_command(self, command):
        """Handle F: file I/O commands"""
        import os
        import pathlib

        cmd = command[2:].strip()
        parts = cmd.split(" ", 2)

        if not parts:
            return "continue"

        operation = parts[0].upper()

        try:
            if operation == "WRITE" and len(parts) >= 3:
                filename = parts[1].strip('"')
                content = parts[2].strip('"')
                content = self.interpreter.interpolate_text(content)

                pathlib.Path(filename).write_text(content, encoding="utf-8")
                self.interpreter.variables["FILE_WRITE_SUCCESS"] = "1"

            elif operation == "READ" and len(parts) >= 3:
                filename = parts[1].strip('"')
                var_name = parts[2].strip()

                if os.path.exists(filename):
                    content = pathlib.Path(filename).read_text(encoding="utf-8")
                    self.interpreter.variables[var_name] = content
                    self.interpreter.variables["FILE_READ_SUCCESS"] = "1"
                else:
                    self.interpreter.variables[var_name] = ""
                    self.interpreter.variables["FILE_READ_SUCCESS"] = "0"

            elif operation == "APPEND" and len(parts) >= 3:
                filename = parts[1].strip('"')
                content = parts[2].strip('"')
                content = self.interpreter.interpolate_text(content)

                with open(filename, "a", encoding="utf-8") as f:
                    f.write(content)
                self.interpreter.variables["FILE_APPEND_SUCCESS"] = "1"

            elif operation == "DELETE" and len(parts) >= 2:
                filename = parts[1].strip('"')
                if os.path.exists(filename):
                    os.remove(filename)
                    self.interpreter.variables["FILE_DELETE_SUCCESS"] = "1"
                else:
                    self.interpreter.variables["FILE_DELETE_SUCCESS"] = "0"

            elif operation == "EXISTS" and len(parts) >= 3:
                filename = parts[1].strip('"')
                var_name = parts[2].strip()
                exists = "1" if os.path.exists(filename) else "0"
                self.interpreter.variables[var_name] = exists

            elif operation == "SIZE" and len(parts) >= 3:
                filename = parts[1].strip('"')
                var_name = parts[2].strip()
                if os.path.exists(filename):
                    size = str(os.path.getsize(filename))
                    self.interpreter.variables[var_name] = size
                else:
                    self.interpreter.variables[var_name] = "0"

        except Exception as e:
            self.interpreter.debug_output(f"File operation error: {e}")

        return "continue"

    def _handle_web_command(self, command):
        """Handle W: web/HTTP commands"""
        import urllib.parse

        cmd = command[2:].strip()

        # Parse arguments respecting quoted strings
        pattern = r'"([^"]*)"|\S+'
        args = []
        for match in re.finditer(pattern, cmd):
            if match.group(1) is not None:  # Quoted string
                args.append(match.group(1))
            else:  # Unquoted word
                args.append(match.group(0))

        if not args:
            return "continue"

        operation = args[0].upper()

        try:
            if operation == "ENCODE" and len(args) >= 3:
                text = args[1]
                var_name = args[2]
                text = self.interpreter.interpolate_text(text)
                encoded = urllib.parse.quote(text)
                self.interpreter.variables[var_name] = encoded

            elif operation == "DECODE" and len(args) >= 3:
                text = args[1]
                var_name = args[2]
                text = self.interpreter.interpolate_text(text)
                decoded = urllib.parse.unquote(text)
                self.interpreter.variables[var_name] = decoded

        except Exception as e:
            self.interpreter.debug_output(f"Web operation error: {e}")

        return "continue"

    def _handle_database_command(self, command):
        """Handle D: database commands"""
        import sqlite3

        cmd = command[2:].strip()
        parts = cmd.split(" ", 1)

        if not parts:
            return "continue"

        operation = parts[0].upper()

        try:
            if operation == "OPEN":
                db_name = parts[1].strip('"') if len(parts) > 1 else "default.db"
                db_name = self.interpreter.interpolate_text(db_name)

                # Store database connection (simplified)
                if not hasattr(self.interpreter, "db_connections"):
                    self.interpreter.db_connections = {}

                try:
                    conn = sqlite3.connect(db_name)
                    self.interpreter.db_connections["current"] = conn
                    self.interpreter.variables["DB_OPEN_SUCCESS"] = "1"
                except sqlite3.Error:
                    self.interpreter.variables["DB_OPEN_SUCCESS"] = "0"

            elif operation == "QUERY" and len(parts) >= 2:
                query = parts[1].strip('"')
                query = self.interpreter.interpolate_text(query)

                if (
                    hasattr(self.interpreter, "db_connections")
                    and "current" in self.interpreter.db_connections
                ):
                    try:
                        conn = self.interpreter.db_connections["current"]
                        cursor = conn.cursor()
                        cursor.execute(query)
                        conn.commit()
                        self.interpreter.variables["DB_QUERY_SUCCESS"] = "1"
                    except sqlite3.Error:
                        self.interpreter.variables["DB_QUERY_SUCCESS"] = "0"
                else:
                    self.interpreter.variables["DB_QUERY_SUCCESS"] = "0"

            elif operation == "INSERT" and len(parts) >= 2:
                # D:INSERT "table" "columns" "values"
                full_parts = cmd.split(" ", 3)
                if len(full_parts) >= 4:
                    table = full_parts[1].strip('"')
                    columns = full_parts[2].strip('"')
                    values = full_parts[3].strip('"')

                    table = self.interpreter.interpolate_text(table)
                    columns = self.interpreter.interpolate_text(columns)
                    values = self.interpreter.interpolate_text(values)

                    query = f"INSERT INTO {table} ({columns}) VALUES ({values})"

                    if (
                        hasattr(self.interpreter, "db_connections")
                        and "current" in self.interpreter.db_connections
                    ):
                        try:
                            conn = self.interpreter.db_connections["current"]
                            cursor = conn.cursor()
                            cursor.execute(query)
                            conn.commit()
                            self.interpreter.variables["DB_INSERT_SUCCESS"] = "1"
                        except sqlite3.Error:
                            self.interpreter.variables["DB_INSERT_SUCCESS"] = "0"
                    else:
                        self.interpreter.variables["DB_INSERT_SUCCESS"] = "0"

        except Exception as e:
            self.interpreter.debug_output(f"Database operation error: {e}")

        return "continue"

    def _handle_string_command(self, command):
        """Handle S: string processing commands"""

        cmd = command[2:].strip()

        # Parse arguments respecting quoted strings
        # Pattern to match quoted strings or unquoted words
        pattern = r'"([^"]*)"|\S+'

        # Extract actual arguments from regex matches
        args = []
        for match in re.finditer(pattern, cmd):
            if match.group(1) is not None:  # Quoted string
                args.append(match.group(1))
            else:  # Unquoted word
                args.append(match.group(0))

        if not args:
            return "continue"

        operation = args[0].upper()

        try:
            if operation == "LENGTH" and len(args) >= 3:
                text = args[1]
                var_name = args[2]
                text = self.interpreter.interpolate_text(text)
                self.interpreter.variables[var_name] = str(len(text))

            elif operation == "UPPER" and len(args) >= 3:
                text = args[1]
                var_name = args[2]
                text = self.interpreter.interpolate_text(text)
                self.interpreter.variables[var_name] = text.upper()

            elif operation == "LOWER" and len(args) >= 3:
                text = args[1]
                var_name = args[2]
                text = self.interpreter.interpolate_text(text)
                self.interpreter.variables[var_name] = text.lower()

            elif operation == "FIND" and len(args) >= 4:
                text = args[1]
                search = args[2]
                var_name = args[3]
                text = self.interpreter.interpolate_text(text)
                search = self.interpreter.interpolate_text(search)
                pos = text.find(search)
                self.interpreter.variables[var_name] = str(pos)

            elif operation == "REPLACE" and len(args) >= 5:
                # S:REPLACE "text" "old" "new" VAR
                text = args[1]
                old = args[2]
                new = args[3]
                var_name = args[4]
                text = self.interpreter.interpolate_text(text)
                old = self.interpreter.interpolate_text(old)
                new = self.interpreter.interpolate_text(new)
                if old:  # Don't replace empty strings
                    result = text.replace(old, new)
                else:
                    result = text
                self.interpreter.variables[var_name] = result

            elif operation == "SUBSTRING" and len(args) >= 5:
                # S:SUBSTRING "text" start length VAR
                text = args[1]
                start = int(args[2])
                length = int(args[3])
                var_name = args[4]
                text = self.interpreter.interpolate_text(text)
                result = text[start : start + length]
                self.interpreter.variables[var_name] = result

            elif operation == "SPLIT" and len(args) >= 4:
                text = args[1]
                delimiter = args[2]
                var_name = args[3]
                text = self.interpreter.interpolate_text(text)
                delimiter = self.interpreter.interpolate_text(delimiter)
                split_parts = text.split(delimiter)
                # Store first part in variable, could be extended
                if split_parts:
                    self.interpreter.variables[var_name] = split_parts[0]
                else:
                    self.interpreter.variables[var_name] = ""

        except (ValueError, IndexError) as e:
            self.interpreter.debug_output(f"String operation error: {e}")

        return "continue"

    def _handle_datetime_command(self, command):
        """Handle DT: date/time commands"""
        from datetime import datetime
        import time

        cmd = command[3:].strip()  # Skip "DT:"
        parts = cmd.split(" ", 2)

        if not parts:
            return "continue"

        operation = parts[0].upper()

        try:
            if operation == "NOW" and len(parts) >= 3:
                format_str = parts[1].strip('"')
                var_name = parts[2].strip()

                # Simple format mapping
                format_map = {
                    "YYYY-MM-DD": "%Y-%m-%d",
                    "HH:MM:SS": "%H:%M:%S",
                    "YYYY-MM-DD HH:MM:SS": "%Y-%m-%d %H:%M:%S",
                }

                fmt = format_map.get(format_str, format_str)
                now = datetime.now().strftime(fmt)
                self.interpreter.variables[var_name] = now

            elif operation == "TIMESTAMP" and len(parts) >= 2:
                var_name = parts[1].strip()
                timestamp = str(int(time.time()))
                self.interpreter.variables[var_name] = timestamp

            elif operation == "PARSE" and len(parts) >= 4:
                date_str = parts[1].strip('"')
                format_str = parts[2].strip('"')
                var_name = parts[3].strip()

                # Simple parsing - just store the original for now
                self.interpreter.variables[var_name] = date_str

            elif operation == "FORMAT" and len(parts) >= 4:
                timestamp = parts[1].strip('"')
                format_str = parts[2].strip('"')
                var_name = parts[3].strip()

                # Try to format timestamp
                try:
                    ts = int(self.interpreter.interpolate_text(timestamp))
                    dt = datetime.fromtimestamp(ts)

                    format_map = {
                        "YYYY-MM-DD": "%Y-%m-%d",
                        "HH:MM:SS": "%H:%M:%S",
                        "YYYY-MM-DD HH:MM:SS": "%Y-%m-%d %H:%M:%S",
                    }

                    fmt = format_map.get(format_str, format_str)
                    formatted = dt.strftime(fmt)
                    self.interpreter.variables[var_name] = formatted
                except (ValueError, OSError):
                    self.interpreter.variables[var_name] = timestamp

        except Exception as e:
            self.interpreter.debug_output(f"DateTime operation error: {e}")

        return "continue"

    def _handle_graphics_command(self, command):
        """Handle G: graphics commands for turtle graphics"""
        cmd = command[2:].strip()  # Skip "G:"
        parts = cmd.split(",")

        if not parts:
            return "continue"

        # Ensure turtle graphics system is initialized
        if not self.interpreter.turtle_graphics:
            self.interpreter.init_turtle_graphics()

        operation = parts[0].upper()

        try:
            if operation == "LINE" and len(parts) >= 5:
                # G:LINE,x1,y1,x2,y2 - draw a line
                x1 = float(parts[1])
                y1 = float(parts[2])
                x2 = float(parts[3])
                y2 = float(parts[4])

                # Move to start position without drawing
                self.interpreter.turtle_setxy(x1, y1)
                self.interpreter.turtle_graphics["pen_down"] = True

                # Draw line to end position
                self.interpreter.turtle_setxy(x2, y2)
                self.interpreter.log_output(f"G:LINE from ({x1},{y1}) to ({x2},{y2})")

            elif operation == "CIRCLE" and len(parts) >= 4:
                # G:CIRCLE,x,y,radius
                x = float(parts[1])
                y = float(parts[2])
                radius = float(parts[3])

                # Move to center, then draw circle
                self.interpreter.turtle_setxy(x, y)
                self.interpreter.turtle_circle(radius)
                self.interpreter.log_output(f"G:CIRCLE at ({x},{y}) radius {radius}")

            elif operation == "RECT" and len(parts) >= 5:
                # G:RECT,x,y,width,height
                x = float(parts[1])
                y = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])

                self.interpreter.log_output(f"G:RECT at ({x},{y}) {width}x{height}")

                # Draw rectangle
                self.interpreter.turtle_setxy(x, y)
                self.interpreter.turtle_graphics["pen_down"] = True
                for _ in range(2):
                    self.interpreter.turtle_forward(width)
                    self.interpreter.turtle_right(90)
                    self.interpreter.turtle_forward(height)
                    self.interpreter.turtle_right(90)

            elif operation == "CLEAR":
                # G:CLEAR - clear graphics screen
                self.interpreter.clear_turtle_screen()
                self.interpreter.log_output("Graphics screen cleared")

            elif operation == "PENUP":
                # G:PENUP - lift pen
                self.interpreter.turtle_graphics["pen_down"] = False
                self.interpreter.log_output("Pen up")

            elif operation == "PENDOWN":
                # G:PENDOWN - lower pen
                self.interpreter.turtle_graphics["pen_down"] = True
                self.interpreter.log_output("Pen down")

            elif operation == "COLOR" and len(parts) >= 2:
                # G:COLOR,color_name
                color = parts[1].strip()
                self.interpreter.turtle_graphics["pen_color"] = color
                self.interpreter.log_output(f"Pen color set to {color}")

            else:
                self.interpreter.log_output(f"Unknown graphics command: {operation}")

        except Exception as e:
            self.interpreter.debug_output(f"Graphics command error: {e}")

        return "continue"

    def _handle_math_command(self, command):
        """Handle MATH: mathematical operations"""
        import math

        cmd = command[5:].strip()  # Skip "MATH:"
        parts = cmd.split(" ", 1)

        if not parts:
            return "continue"

        operation = parts[0].upper()

        try:
            if operation == "SIN" and len(parts) > 1:
                angle = float(self.interpreter.evaluate_expression(parts[1]))
                result = math.sin(math.radians(angle))
                self.interpreter.variables["MATH_RESULT"] = result
                self.interpreter.log_output(f"MATH:SIN({angle}°) = {result:.4f}")

            elif operation == "COS" and len(parts) > 1:
                angle = float(self.interpreter.evaluate_expression(parts[1]))
                result = math.cos(math.radians(angle))
                self.interpreter.variables["MATH_RESULT"] = result
                self.interpreter.log_output(f"MATH:COS({angle}°) = {result:.4f}")

            elif operation == "TAN" and len(parts) > 1:
                angle = float(self.interpreter.evaluate_expression(parts[1]))
                result = math.tan(math.radians(angle))
                self.interpreter.variables["MATH_RESULT"] = result
                self.interpreter.log_output(f"MATH:TAN({angle}°) = {result:.4f}")

            elif operation == "SQRT" and len(parts) > 1:
                value = float(self.interpreter.evaluate_expression(parts[1]))
                if value >= 0:
                    result = math.sqrt(value)
                    self.interpreter.variables["MATH_RESULT"] = result
                    self.interpreter.log_output(f"MATH:SQRT({value}) = {result:.4f}")
                else:
                    self.interpreter.log_output("MATH:SQRT requires non-negative value")

            elif operation == "POWER" and len(parts) > 1:
                expr_parts = parts[1].split(",")
                if len(expr_parts) == 2:
                    base = float(
                        self.interpreter.evaluate_expression(expr_parts[0].strip())
                    )
                    exp = float(
                        self.interpreter.evaluate_expression(expr_parts[1].strip())
                    )
                    result = math.pow(base, exp)
                    self.interpreter.variables["MATH_RESULT"] = result
                    self.interpreter.log_output(
                        f"MATH:POWER({base},{exp}) = {result:.4f}"
                    )

            elif operation == "LOG" and len(parts) > 1:
                value = float(self.interpreter.evaluate_expression(parts[1]))
                if value > 0:
                    result = math.log10(value)
                    self.interpreter.variables["MATH_RESULT"] = result
                    self.interpreter.log_output(f"MATH:LOG({value}) = {result:.4f}")
                else:
                    self.interpreter.log_output("MATH:LOG requires positive value")

            elif operation == "LN" and len(parts) > 1:
                value = float(self.interpreter.evaluate_expression(parts[1]))
                if value > 0:
                    result = math.log(value)
                    self.interpreter.variables["MATH_RESULT"] = result
                    self.interpreter.log_output(f"MATH:LN({value}) = {result:.4f}")
                else:
                    self.interpreter.log_output("MATH:LN requires positive value")

            elif operation == "ABS" and len(parts) > 1:
                value = float(self.interpreter.evaluate_expression(parts[1]))
                result = abs(value)
                self.interpreter.variables["MATH_RESULT"] = result
                self.interpreter.log_output(f"MATH:ABS({value}) = {result}")

            elif operation == "ROUND" and len(parts) > 1:
                expr_parts = parts[1].split(",")
                value = float(
                    self.interpreter.evaluate_expression(expr_parts[0].strip())
                )
                decimals = int(expr_parts[1].strip()) if len(expr_parts) > 1 else 0
                result = round(value, decimals)
                self.interpreter.variables["MATH_RESULT"] = result
                self.interpreter.log_output(
                    f"MATH:ROUND({value},{decimals}) = {result}"
                )

            elif operation == "RANDOM":
                expr_parts = parts[1].split(",") if len(parts) > 1 else []
                if len(expr_parts) == 2:
                    min_val = float(
                        self.interpreter.evaluate_expression(expr_parts[0].strip())
                    )
                    max_val = float(
                        self.interpreter.evaluate_expression(expr_parts[1].strip())
                    )
                    result = random.uniform(min_val, max_val)
                else:
                    result = random.random()
                self.interpreter.variables["MATH_RESULT"] = result
                self.interpreter.log_output(f"MATH:RANDOM = {result:.4f}")

        except Exception as e:
            self.interpreter.debug_output(f"MATH operation error: {e}")

        return "continue"

    def _handle_branch_command(self, command):
        """Handle BRANCH: advanced branching operations"""
        cmd = command[7:].strip()  # Skip "BRANCH:"
        parts = cmd.split(" ", 1)

        if not parts:
            return "continue"

        operation = parts[0].upper()

        try:
            if operation == "MULTI":
                # BRANCH:MULTI condition1:label1, condition2:label2, ...
                if len(parts) > 1:
                    conditions_str = parts[1]
                    conditions = [c.strip() for c in conditions_str.split(",")]

                    for condition_pair in conditions:
                        if ":" in condition_pair:
                            cond_expr, label = condition_pair.split(":", 1)
                            cond_expr = cond_expr.strip()
                            label = label.strip()

                            try:
                                cond_val = self.interpreter.evaluate_expression(
                                    cond_expr
                                )
                                if cond_val:
                                    if label in self.interpreter.labels:
                                        self.interpreter.debug_output(
                                            f"BRANCH:MULTI condition '{cond_expr}' true, jumping to {label}"
                                        )
                                        return f"jump:{self.interpreter.labels[label]}"
                                    else:
                                        self.interpreter.debug_output(
                                            f"BRANCH:MULTI label '{label}' not found"
                                        )
                            except Exception as e:
                                self.interpreter.debug_output(
                                    f"BRANCH:MULTI condition error: {e}"
                                )

            elif operation == "RANGE":
                # BRANCH:RANGE value, min:max:label, min2:max2:label2, ...
                if len(parts) > 1:
                    args = parts[1].split(",", 1)
                    if len(args) == 2:
                        value_expr = args[0].strip()
                        ranges_str = args[1]

                        try:
                            value = float(
                                self.interpreter.evaluate_expression(value_expr)
                            )

                            ranges = [r.strip() for r in ranges_str.split(",")]
                            for range_spec in ranges:
                                if ":" in range_spec:
                                    range_part, label = range_spec.rsplit(":", 1)
                                    range_part = range_part.strip()
                                    label = label.strip()

                                    if "-" in range_part:
                                        min_str, max_str = range_part.split("-", 1)
                                        min_val = float(
                                            self.interpreter.evaluate_expression(
                                                min_str.strip()
                                            )
                                        )
                                        max_val = float(
                                            self.interpreter.evaluate_expression(
                                                max_str.strip()
                                            )
                                        )

                                        if min_val <= value <= max_val:
                                            if label in self.interpreter.labels:
                                                self.interpreter.debug_output(
                                                    f"BRANCH:RANGE {value} in [{min_val},{max_val}], jumping to {label}"
                                                )
                                                return f"jump:{self.interpreter.labels[label]}"
                                            else:
                                                self.interpreter.debug_output(
                                                    f"BRANCH:RANGE label '{label}' not found"
                                                )
                        except Exception as e:
                            self.interpreter.debug_output(f"BRANCH:RANGE error: {e}")

            elif operation == "CASE":
                # BRANCH:CASE value, case1:label1, case2:label2, default:label
                if len(parts) > 1:
                    args = parts[1].split(",", 1)
                    if len(args) == 2:
                        value_expr = args[0].strip()
                        cases_str = args[1]

                        try:
                            value = self.interpreter.evaluate_expression(value_expr)
                            value_str = str(value).strip()

                            cases = [c.strip() for c in cases_str.split(",")]
                            default_label = None

                            for case_spec in cases:
                                if ":" in case_spec:
                                    case_part, label = case_spec.split(":", 1)
                                    case_part = case_part.strip()
                                    label = label.strip()

                                    if case_part.upper() == "DEFAULT":
                                        default_label = label
                                    elif case_part.strip(
                                        '"'
                                    ) == value_str or case_part == str(value):
                                        if label in self.interpreter.labels:
                                            self.interpreter.debug_output(
                                                f"BRANCH:CASE {value} matches '{case_part}', jumping to {label}"
                                            )
                                            return (
                                                f"jump:{self.interpreter.labels[label]}"
                                            )
                                        else:
                                            self.interpreter.debug_output(
                                                f"BRANCH:CASE label '{label}' not found"
                                            )

                            # If no case matched and we have a default
                            if (
                                default_label
                                and default_label in self.interpreter.labels
                            ):
                                self.interpreter.debug_output(
                                    f"BRANCH:CASE {value} using default, jumping to {default_label}"
                                )
                                return f"jump:{self.interpreter.labels[default_label]}"

                        except Exception as e:
                            self.interpreter.debug_output(f"BRANCH:CASE error: {e}")

        except Exception as e:
            self.interpreter.debug_output(f"BRANCH operation error: {e}")

        return "continue"

    def _handle_multimedia_command(self, command):
        """Handle MULTIMEDIA: multimedia operations"""
        cmd = command[11:].strip()  # Skip "MULTIMEDIA:"
        parts = cmd.split(" ", 1)

        if not parts:
            return "continue"

        operation = parts[0].upper()

        try:
            if operation == "PLAYSOUND":
                # MULTIMEDIA:PLAYSOUND "filename" [,duration]
                if len(parts) > 1:
                    args = parts[1].split(",", 1)
                    filename = args[0].strip('"')
                    duration = float(args[1].strip()) if len(args) > 1 else None

                    self.interpreter.log_output(
                        f"MULTIMEDIA: Playing sound '{filename}'{' for ' + str(duration) + 's' if duration else ''}"
                    )

            elif operation == "SHOWIMAGE":
                # MULTIMEDIA:SHOWIMAGE "filename", x, y [,width, height]
                if len(parts) > 1:
                    args = [a.strip() for a in parts[1].split(",")]
                    if len(args) >= 3:
                        filename = args[0].strip('"')
                        x = float(args[1])
                        y = float(args[2])
                        width = float(args[3]) if len(args) > 3 else None
                        height = float(args[4]) if len(args) > 4 else None

                        self.interpreter.log_output(
                            f"MULTIMEDIA: Showing image '{filename}' at ({x},{y}){' size ' + str(width) + 'x' + str(height) if width and height else ''}"
                        )

            elif operation == "PLAYVIDEO":
                # MULTIMEDIA:PLAYVIDEO "filename" [,x, y, width, height]
                if len(parts) > 1:
                    args = [a.strip() for a in parts[1].split(",")]
                    filename = args[0].strip('"')
                    x = float(args[1]) if len(args) > 1 else 0
                    y = float(args[2]) if len(args) > 2 else 0
                    width = float(args[3]) if len(args) > 3 else None
                    height = float(args[4]) if len(args) > 4 else None

                    self.interpreter.log_output(
                        f"MULTIMEDIA: Playing video '{filename}' at ({x},{y}){' size ' + str(width) + 'x' + str(height) if width and height else ''}"
                    )

            elif operation == "TEXTTOSPEECH":
                # MULTIMEDIA:TEXTTOSPEECH "text" [,voice, speed]
                if len(parts) > 1:
                    args = [a.strip() for a in parts[1].split(",", 2)]
                    text = args[0].strip('"')
                    voice = args[1].strip('"') if len(args) > 1 else "default"
                    speed = float(args[2]) if len(args) > 2 else 1.0

                    self.interpreter.log_output(
                        f"MULTIMEDIA: Speaking '{text}' with voice '{voice}' at speed {speed}"
                    )

            elif operation == "RECORD":
                # MULTIMEDIA:RECORD AUDIO|VIDEO, "filename", duration
                if len(parts) > 1:
                    args = [a.strip() for a in parts[1].split(",", 2)]
                    if len(args) >= 3:
                        media_type = args[0].upper()
                        filename = args[1].strip('"')
                        duration = float(args[2])

                        self.interpreter.log_output(
                            f"MULTIMEDIA: Recording {media_type} to '{filename}' for {duration}s"
                        )

        except Exception as e:
            self.interpreter.debug_output(f"MULTIMEDIA operation error: {e}")

        return "continue"

    def _handle_storage_command(self, command):
        """Handle STORAGE: advanced variable storage operations"""
        cmd = command[8:].strip()  # Skip "STORAGE:"
        parts = cmd.split(" ", 1)

        if not parts:
            return "continue"

        operation = parts[0].upper()

        try:
            if operation == "SAVE":
                # STORAGE:SAVE "filename"
                if len(parts) > 1:
                    filename = parts[1].strip('"')
                    filename = self.interpreter.interpolate_text(filename)

                    # Save all variables to a JSON file
                    import json

                    try:
                        with open(filename, "w", encoding="utf-8") as f:
                            # Create a copy
                            # without internal interpreter variables
                            save_vars = {
                                k: v
                                for k, v in self.interpreter.variables.items()
                                if not k.startswith("_")
                                and k not in ["RESULT", "MATH_RESULT"]
                            }
                            json.dump(save_vars, f, indent=2, default=str)
                        self.interpreter.variables["STORAGE_SUCCESS"] = "1"
                        self.interpreter.log_output(
                            f"STORAGE: Variables saved to '{filename}'"
                        )
                    except Exception as e:
                        self.interpreter.variables["STORAGE_SUCCESS"] = "0"
                        self.interpreter.debug_output(f"STORAGE:SAVE error: {e}")

            elif operation == "LOAD":
                # STORAGE:LOAD "filename"
                if len(parts) > 1:
                    filename = parts[1].strip('"')
                    filename = self.interpreter.interpolate_text(filename)

                    import json

                    try:
                        with open(filename, "r", encoding="utf-8") as f:
                            loaded_vars = json.load(f)
                            self.interpreter.variables.update(loaded_vars)
                        self.interpreter.variables["STORAGE_SUCCESS"] = "1"
                        self.interpreter.log_output(
                            f"STORAGE: Variables loaded from '{filename}'"
                        )
                    except Exception as e:
                        self.interpreter.variables["STORAGE_SUCCESS"] = "0"
                        self.interpreter.debug_output(f"STORAGE:LOAD error: {e}")

            elif operation == "LIST":
                # STORAGE:LIST [pattern]
                pattern = parts[1].strip('"') if len(parts) > 1 else None

                var_list = []
                for name, value in self.interpreter.variables.items():
                    if not name.startswith("_"):  # Skip internal variables
                        if pattern is None or pattern in name:
                            var_list.append(f"{name} = {value}")

                if var_list:
                    self.interpreter.log_output("STORAGE: Variables:")
                    for var_info in var_list[:20]:  # Limit to first 20
                        self.interpreter.log_output(f"  {var_info}")
                    if len(var_list) > 20:
                        self.interpreter.log_output(
                            f"  ... and {len(var_list) - 20} more"
                        )
                else:
                    self.interpreter.log_output("STORAGE: No variables found")

            elif operation == "DELETE":
                # STORAGE:DELETE var1, var2, ...
                if len(parts) > 1:
                    var_names = [v.strip() for v in parts[1].split(",")]
                    deleted_count = 0
                    for var_name in var_names:
                        if var_name in self.interpreter.variables:
                            del self.interpreter.variables[var_name]
                            deleted_count += 1

                    self.interpreter.log_output(
                        f"STORAGE: Deleted {deleted_count} variable(s)"
                    )

            elif operation == "COUNT":
                # STORAGE:COUNT
                user_vars = [
                    name
                    for name in self.interpreter.variables.keys()
                    if not name.startswith("_")
                ]
                count = len(user_vars)
                self.interpreter.variables["VAR_COUNT"] = count
                self.interpreter.log_output(f"STORAGE: {count} user variables")

            elif operation == "ARRAY":
                # STORAGE:ARRAY name, size [,default_value]
                if len(parts) > 1:
                    args = [a.strip() for a in parts[1].split(",", 2)]
                    if len(args) >= 2:
                        array_name = args[0]
                        size = int(self.interpreter.evaluate_expression(args[1]))
                        default_value = (
                            self.interpreter.evaluate_expression(args[2])
                            if len(args) > 2
                            else 0
                        )

                        array = [default_value] * size
                        self.interpreter.variables[array_name] = array
                        self.interpreter.log_output(
                            f"STORAGE: Created array '{array_name}' with {size} elements"
                        )

        except Exception as e:
            self.interpreter.debug_output(f"STORAGE operation error: {e}")

        return "continue"

    # PILOT 73 Command Handlers

    def _handle_dimension_array(self, command):
        """Handle D: dimension array command (PILOT 73)"""
        array_spec = command[2:].strip()

        # Parse array specification: NAME(SIZE) or #NAME(SIZE) for numeric
        if "(" in array_spec and ")" in array_spec:
            name_part, size_part = array_spec.split("(", 1)
            size_str = size_part.rstrip(")")

            try:
                size = int(size_str)
                if size <= 0:
                    self.interpreter.debug_output(
                        f"Error: Array size must be positive, got {size}"
                    )
                    return "continue"

                array_name = name_part.strip()
                # Initialize array with None values
                # (PILOT 73 arrays are 1-indexed)
                self.arrays[array_name] = [None] * (size + 1)

                self.interpreter.debug_output(
                    f"[DEBUG] Created array {array_name} with size {size}"
                )
                return "continue"
            except ValueError:
                self.interpreter.debug_output(f"Error: Invalid array size '{size_str}'")
                return "continue"
        else:
            self.interpreter.debug_output(
                f"Error: Invalid array specification '{array_spec}'"
            )
            return "continue"

    def _handle_pause(self, command):
        """Handle PA: pause command (PILOT 73)"""
        duration = command[3:].strip()
        if duration:
            try:
                seconds = float(duration)
                import time

                time.sleep(seconds)
                self.interpreter.debug_output(f"[DEBUG] Paused for {seconds} seconds")
            except ValueError:
                self.interpreter.debug_output(
                    f"Error: Invalid pause duration '{duration}'"
                )
        else:
            # Default pause - wait for user input
            self.interpreter.get_user_input("Press Enter to continue...")
        return "continue"

    def _handle_clear_home(self, command):
        """Handle CH: clear home command (PILOT 73)"""
        # Clear screen and move cursor to home position
        self.screen_control["screen_cleared"] = True
        self.screen_control["cursor_row"] = 0
        self.screen_control["cursor_col"] = 0
        # In a real implementation, this would clear the terminal/console
        self.interpreter.log_output("\n" * 50)  # Simple screen clear simulation
        self.interpreter.debug_output("[DEBUG] Screen cleared and cursor homed")
        return "continue"

    def _handle_cursor_address(self, command):
        """Handle CA: cursor address command (PILOT 73)"""
        coords = command[3:].strip()
        if "," in coords:
            try:
                row_str, col_str = coords.split(",", 1)
                row = int(row_str.strip())
                col = int(col_str.strip())
                self.screen_control["cursor_row"] = row
                self.screen_control["cursor_col"] = col
                self.interpreter.debug_output(f"[DEBUG] Cursor moved to ({row}, {col})")
            except ValueError:
                self.interpreter.debug_output(
                    f"Error: Invalid cursor coordinates '{coords}'"
                )
        else:
            self.interpreter.debug_output(
                f"Error: Invalid cursor address format '{coords}'"
            )
        return "continue"

    def _handle_clear_line(self, command):
        """Handle CL: clear line command (PILOT 73)"""
        # Clear from cursor to end of line
        self.interpreter.debug_output("[DEBUG] Line cleared from cursor")
        return "continue"

    def _handle_clear_end(self, command):
        """Handle CE: clear to end command (PILOT 73)"""
        # Clear from cursor to end of screen
        self.interpreter.debug_output("[DEBUG] Cleared from cursor to end of screen")
        return "continue"

    def _handle_jump_match(self, command):
        """Handle JM: jump match command (PILOT 73)"""
        args = command[3:].strip()
        if not args:
            self.interpreter.debug_output("Error: JM requires label arguments")
            return "continue"

        labels = [label.strip() for label in args.split(",")]

        # In PILOT 73, JM jumps based on which pattern matched
        # For simplicity, we'll use the match number from system variables
        match_num = self.system_vars.get("match_number", 0)

        if 1 <= match_num <= len(labels):
            target_label = labels[match_num - 1]
            if target_label in self.interpreter.labels:
                return f"jump:{self.interpreter.labels[target_label]}"
            else:
                self.interpreter.debug_output(
                    f"Error: JM target label '{target_label}' not found"
                )

        return "continue"

    def _handle_type_hang(self, command):
        """Handle TH: type hang command (PILOT 73)"""
        text = command[3:].strip()
        text = self.interpreter.interpolate_text(text)
        # Type without newline
        self.interpreter.log_output(text, end="")
        return "continue"

    def _handle_system_command(self, command):
        """Handle XS: system command (PILOT 73)"""
        cmd = command[3:].strip()
        if cmd:
            try:
                import subprocess

                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.system_vars["status"] = result.returncode
                if result.stdout:
                    self.interpreter.log_output(result.stdout)
                if result.stderr:
                    self.interpreter.debug_output(
                        f"System command stderr: {result.stderr}"
                    )
            except Exception as e:
                self.interpreter.debug_output(f"Error executing system command: {e}")
                self.system_vars["status"] = -1
        return "continue"

    def _handle_problem(self, command):
        """Handle PR: problem command (PILOT 73)"""
        # Mark problem sections - implementation dependent
        problem_text = command[3:].strip()
        self.interpreter.debug_output(f"[PROBLEM] {problem_text}")
        return "continue"
